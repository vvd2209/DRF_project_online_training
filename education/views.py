from requests import Response
from django.db.models.functions import datetime
from django.utils import timezone
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from education.services import create_product, create_price
from education.tasks import check_update_course
from education.models import Lesson, Course, Payment
from education.paginators import ListPaginator
from education.permissions import IsModerator, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, PaymentCreateSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ Контроллер для курса """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    perms_methods = {
        'list': [IsAuthenticated, IsModerator | IsAdminUser],
        'retrieve': [IsAuthenticated, IsOwner | IsModerator | IsAdminUser],
        'create': [IsAuthenticated, ~IsModerator],
        'update': [IsAuthenticated, IsOwner | IsModerator],
        'partial_update': [IsAuthenticated, IsOwner | IsModerator],
        'destroy': [IsAuthenticated, IsOwner | IsAdminUser],
    }
    pagination_class = ListPaginator

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course_update = serializer.save()
        if course_update:
            check_update_course.delay(course_update.course_id)


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    """ Просмотр списка всех уроков """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
    pagination_class = ListPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Изменение урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'pay_type']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(APIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        # Получаем данные о платеже из запроса
        user = request.user
        amount = request.data.get('amount')
        pay_type = request.data.get('pay_type')

        # Создаем продукт в Stripe
        product_id = create_product("Course Subscription", "Subscription to course")

        # Создаем цену в Stripe
        price_id = create_price(product_id, amount, 'RUB')

        # Установка текущей даты и времени для поля payment_date
        payment_date = timezone.now()

        # Создаем запись о платеже в нашей системе
        payment = Payment.objects.create(user=user, amount=amount, pay_type=pay_type,
                                          product_id=product_id, price_id=price_id, payment_date=payment_date)

        # Создаем сессию для платежа в Stripe
        success_url = "http://example.com/success"  # Замените на ваш URL успешного платежа
        cancel_url = "http://example.com/cancel"  # Замените на ваш URL отмены платежа
        session_url = payment.create_checkout_session(success_url, cancel_url)

        if session_url:
            # Если сессия создана успешно, возвращаем URL для оплаты
            return Response({'session_url': session_url}, status=status.HTTP_201_CREATED)
        else:
            # Если возникла ошибка при создании сессии, возвращаем соответствующий ответ
            return Response({'error': 'Failed to create checkout session'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusAPIView(APIView):
    def get(self, request, pk, format=None):
        # Получаем запись о платеже по его идентификатору
        payment = Payment.objects.get(pk=pk)

        # Получаем данные о статусе платежа из Stripe
        # В этом месте мы можем добавить логику для проверки статуса платежа в Stripe
        # Возвращаем данные о статусе платежа в ответе
        return Response({'status': 'Payment status goes here'}, status=status.HTTP_200_OK)
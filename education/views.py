import os
import stripe
from requests import Response
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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


class PaymentListAPIView(generics.ListAPIView):
    """ Список платежей """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('payment_date',)
    pagination_class = ListPaginator


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        stripe.api_key = os.getenv("STRIPE_API_KEY")
        course_id = request.data.get("course")

        user = self.request.user
        data = {"user": user.id, "course": course_id, "is_confirmed": True}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
        )

        stripe.PaymentIntent.confirm(
            response.id,
            payment_method="pm_card_visa",
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

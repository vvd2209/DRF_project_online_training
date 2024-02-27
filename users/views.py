from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from education.models import Payment, Course
from education.permissions import IsSelfUser, IsModerator
from users.models import User, Subscription
from users.serializers import PaymentSerializer, UserSerializer, SubscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    default_serializer = UserSerializer
    queryset = User.objects.all()
    perms_methods = {
        'create': [AllowAny],
        'update': [IsAuthenticated, IsSelfUser | IsAdminUser],
        'partial_update': [IsAuthenticated, IsSelfUser | IsAdminUser],
        'destroy': [IsAuthenticated, IsSelfUser | IsAdminUser],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        password = serializer.validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionCreateAPIView(CreateAPIView):
    """ Класс для создания подписки """

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()


class SubscriptionListAPIView(generics.ListAPIView):
    """ Класс для вывода списка подписок """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [AllowAny]


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """ Класс для изменения подписки """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        subscription = Subscription.objects.filter(course=course, user=user).first()

        if subscription.is_subscribed:
            subscription.is_subscribed = True
            subscription.save()
            message = 'Вы подписались на курс.'

        return Response({"detail": message})


class SubscriptionDestroyAPIView(DestroyAPIView):
    """ Класс для удаления подписки """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        subscription = Subscription.objects.filter(course=course, user=user).first()

        if subscription.is_subscribed:
            subscription.is_subscribed = False
            subscription.save()
            message = 'Вы отписались от курса.'

        return Response({"detail": message})

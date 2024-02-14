from django.shortcuts import render
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

import education
from education.models import Lesson, Course, Payment
from education.permissions import IsModerator, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


class LessonListAPIView(generics.ListAPIView):
    """ Просмотр списка всех уроков """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        education.send_mail.delay(new_lesson.course_id)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Изменение урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    """ Список платежей """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('payment_date',)

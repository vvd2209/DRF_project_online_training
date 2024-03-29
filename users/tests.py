from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from education.models import Lesson, Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """
        Создание тестового пользователя
        """
        self.user = User.objects.create(email='test@test.test', is_active=True, is_superuser=True, is_staff=True,)
        self.user.set_password('test_password')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Тестовый курс')
        self.lesson = Lesson.objects.create(
            name='Тестовый урок',
            description='Тестовое описание',
            course=self.course,
            owner=self.user,
        )

    def test_subscription_create(self):
        """
        Тест создания подписки на курс
        """
        data = {
            'course': self.course.pk,
            'user': self.user.pk
        }

        response = self.client.post(
            reverse('users:subscription_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        """
        Тест на удаление подписки
        """
        moderator_group, created = Group.objects.get_or_create(name='MODERATOR')

        self.user.groups.add(moderator_group)  # Устанавливаем пользователя как модератора
        self.user.save()

        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )
        response = self.client.delete(reverse('users:subscription_delete', args=[subscription.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

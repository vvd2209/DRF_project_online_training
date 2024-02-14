from django.contrib.auth.models import AbstractUser
from django.db import models

from users.servises import NULLABLE
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    EDITOR = 'editor', _('editor')
    MEMBER = 'member', _('member')

class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    city = models.CharField(max_length=50, verbose_name='Город')
    country = models.CharField(max_length=50, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    role = models.CharField(default=UserRoles.MEMBER, choices=UserRoles.choices, verbose_name='Роль пользователя')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    course_name = models.CharField(max_length=300, verbose_name='Название подписки', **NULLABLE)
    course = models.ForeignKey('education.Course', on_delete=models.CASCADE, verbose_name='Курс для подписки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка оформлена')

    def __str__(self):
        return f'{self.course} {self.user}'

    def save(self, *args, **kwargs):
        self.course_name = self.course.title

        return super(Subscription, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курс'

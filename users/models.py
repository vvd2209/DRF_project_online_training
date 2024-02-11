from django.contrib.auth.models import AbstractUser
from django.db import models

from users.servises import NULLABLE


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='телефон')
    city = models.CharField(max_length=50, verbose_name='город')
    country = models.CharField(max_length=50, verbose_name='страна')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

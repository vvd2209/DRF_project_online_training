from django.db import models

from users.models import User
from users.servises import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='education/', verbose_name='превью (картинка)', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец курса', **NULLABLE)

    def __str__(self):
        return f' {self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='education/', verbose_name='превью (картинка)', **NULLABLE)
    video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец урока', **NULLABLE)

    def __str__(self):
        return f' {self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

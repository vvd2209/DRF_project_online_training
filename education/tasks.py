from celery import shared_task
from django.core.mail import send_mail

from education.models import Course
from users.models import Subscription


@shared_task
def check_update_course(pk):
    """
    Уведомление подписчиков об изменениях в курсе
    """
    course = Course.objects.get(pk=pk)
    subscriptions = Subscription.objects.filter(course=course)

    if subscriptions:
        for subscription in subscriptions:
            send_mail(f"Обновление курса",
                      f"Привет, {subscription.user}! В курсе {course.name} произошло обновление!",
                      subscription.user.email,
                      )

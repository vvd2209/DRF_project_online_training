from celery import shared_task

from education.models import Course
from users.models import Subscription


@shared_task
def send_mail(course_id):
    """
    Уведомление подписчиков об изменениях в курсе
    """
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course_id)
    for subscription in subscriptions:
        print(f'Добрый день, {subscription.user}! В курсе "{course.title}" произошло обновление.'
              f'Узнай, что изменилось!')

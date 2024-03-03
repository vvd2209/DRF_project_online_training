from datetime import datetime

import pytz
from celery import shared_task

from users.models import User


@shared_task
def block_user():
    """
    Проверка пользователей на активность.
    Если пользователь не заходил более месяца, он блокируется
    """
    users_is_active = User.objects.filter(is_active=True)

    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_time_now = datetime.datetime.now()
    date_now = date_time_now.astimezone(moscow_timezone)

    for user in users_is_active:
        if user.last_login:
            user_last_login = user.last_login.astimezone(moscow_timezone)
            if (date_now.date() - user_last_login.date()).days > 30:
                user.is_active = False
                user.save()
        else:
            user.last_login = date_now
            user.save()

import json
import os
from datetime import datetime, timedelta
import stripe
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='Importing contacts',  # simply describes this periodic task.
        task='proj.tasks.import_contacts',  # name of task.
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )


stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_product(name, description):
    """Создать продукт в Stripe."""
    product = stripe.Product.create(
        name=name,
        description=description
    )
    return product.id


def create_price(product_id, price_amount, currency):
    """Создать цену в Stripe."""
    if price_amount is not None:
        price_amount = int(price_amount) * 100  # Цены в Stripe указываются в копейках
        price = stripe.Price.create(
            product=product_id,
            unit_amount=price_amount,
            currency=currency
        )
        return price.id
    else:
        # Обработка случая, когда price_amount равно None
        return None


def create_checkout_session(price_id, success_url, cancel_url):
    """Создать сессию для платежа в Stripe."""
    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1
            }
        ],
        mode="payment"
    )
    return session.url

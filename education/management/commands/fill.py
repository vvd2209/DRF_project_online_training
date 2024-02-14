from django.core.management import BaseCommand

from education.models import Course, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_date = [
            {"course": Course.objects.get(pk=1),
             "payment_date": "2024-02-01",
             "amount": 1000,
             "pay_type": 'cash'
             },
            {"course": Course.objects.get(pk=2),
             "payment_date": "2024-02-05",
             "amount": 2000,
             "pay_type": 'cash'
             },
            {"course": Course.objects.get(pk=3),
             "payment_date": "2024-02-07",
             "amount": 3000,
             "pay_type": 'card'
             },
            {"course": Course.objects.get(pk=4),
             "payment_date": "2024-02-10",
             "amount": 4000,
             "pay_type": 'cash'
             },
            {"course": Course.objects.get(pk=5),
             "payment_date": "2024-02-13",
             "amount": 5000,
             "pay_type": 'card'
             }
        ]

        payment_for_create = []

        for data in payment_date:
            payment_for_create.append(Payment(**data))

        Payment.objects.bulk_create(payment_for_create)

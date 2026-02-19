from django.db import transaction
from django.utils import timezone
from .models import Subscription
from billing.models import Invoice

@transaction.atomic
def create_subscription_with_invoice(member, plan, start_date=None):
    if start_date is None:
        start_date = timezone.localdate()

    end_date = Subscription.calc_end_date(start_date, plan.days)

    sub = Subscription.objects.create(
        member=member,
        plan=plan,
        start_date=start_date,
        end_date=end_date,
        status="ACTIVE",
    )

    inv = Invoice.objects.create(
        member=member,
        subscription=sub,
        total_iqd=plan.price_iqd,
        paid_iqd=0,
        balance_iqd=plan.price_iqd,
        status="UNPAID",
    )
    return sub, inv

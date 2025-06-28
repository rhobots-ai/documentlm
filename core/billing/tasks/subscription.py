from calendar import monthrange
from datetime import datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone

from billing.models import Subscription, SubscriptionTokenAllocation
from billing.services import disable_all_active_token_allocations


@shared_task
def allocate_tokens_for_annual_subscriptions_monthly():
    today = datetime.now().today()
    current_day = today.day
    last_day_of_month = monthrange(today.year, today.month)[1]

    # Match the exact day OR handle edge cases for 29/30/31
    subscriptions = Subscription.objects.filter(
        status='active',
        plan__interval='yearly',
        current_start__lte=today,
        current_end__gte=today
    ).filter(
        Q(current_start__day=current_day) |
        (
                Q(current_start__day__gte=28) &
                Q(current_start__day__gt=last_day_of_month) &
                Q(current_start__day=last_day_of_month)
        )
    )

    for subscription in subscriptions:
        user = subscription.user
        plan = subscription.plan

        # Prevent duplicate allocations in the same month
        if SubscriptionTokenAllocation.objects.filter(
                user=user,
                source=SubscriptionTokenAllocation.SourceChoices.SUBSCRIPTION_PURCHASE,
                created_at__year=today.year,
                created_at__month=today.month
        ).exists():
            continue

        disable_all_active_token_allocations(subscription.user)

        SubscriptionTokenAllocation.objects.create(
            user=user,
            source=SubscriptionTokenAllocation.SourceChoices.SUBSCRIPTION_PURCHASE,
            tokens_granted=plan.tokens,
            invoice=None,
            expires_at=(today + relativedelta(months=1)).date()
        )

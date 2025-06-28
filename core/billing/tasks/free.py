from celery import shared_task
from django.contrib.auth import get_user_model

from billing.services import get_subscription, create_free_plan_allocation


@shared_task
def create_daily_free_token_allocation():
    users = get_user_model().objects.filter(is_active=True, is_signed_up=True)

    for user in users:
        subscription = get_subscription(user)
        is_free_plan = not subscription or not subscription.is_active

        if is_free_plan:
            create_free_plan_allocation(user)

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, Max

from billing.models import SubscriptionTokenTransaction, SubscriptionTokenAllocation


def get_token_usage(user: get_user_model()):
    # 1. Active allocations: is_deallocated=False
    active_allocations = user.token_allocations.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=datetime.now().date()),
        is_deallocated=False
    ).aggregate(
        total_granted=Sum('tokens_granted'),
        latest_expires_at=Max('expires_at')
    )
    total = active_allocations['total_granted'] or 0

    # 2. All allocations: for tokens_used
    all_used = user.token_allocations.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=datetime.now().date()),
    ).aggregate(
        total_used=Sum('tokens_used')
    )
    used = all_used['total_used'] or 0

    # 3. Combine results
    allocations = {
        'total': total,
        'used': used,
        'remaining': total - used,
        'expires_at': active_allocations['latest_expires_at']
    }

    return allocations


def get_tokens_used_this_month(user: get_user_model()):
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return SubscriptionTokenTransaction.objects.filter(
        allocation__user=user,
        created_at__gte=start_of_month,
        transaction_type=SubscriptionTokenTransaction.API_CHARGE,
        allocation__source__in=[
            SubscriptionTokenAllocation.SourceChoices.FREE_DAILY
        ]
    ).aggregate(total=Sum('tokens'))['total'] or 0

from contextlib import contextmanager
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F, Q

from billing.models import APILog, APIWalletTransaction, SubscriptionTokenTransaction, SubscriptionTokenAllocation, SubscriptionUsageLog
from billing.services import update_api_wallet


@contextmanager
def log_usage(user: get_user_model(), endpoint: str, is_platform: bool = False):
    """
    Context manager to log API calls and deduct costs from wallet.
    Usage:
        with log_api_call(user, "/chat/completions") as log:
            # Execute API logic here
            log.extra_data = {"request": request_data, "response": response_data}
    """
    if is_platform:
        yield from _log_api_usage(user, endpoint)
    else:
        yield from _los_subscription_usage(user, endpoint)


def _log_api_usage(user: get_user_model(), endpoint: str):
    log = APILog(
        user=user,
        endpoint=endpoint,
        input_tokens=0,
        output_tokens=0,
        input_cost=0,
        output_cost=0,
        total_cost=0,
    )

    try:
        yield log  # Let the wrapped code execute
    except Exception as e:
        log.error_message = str(e)
        log.status = 500
        raise  # Re-raise the exception
    finally:
        # Calculate costs based on user's pricing
        pricing = user.pricing
        input_cost = log.input_tokens * pricing.input_price_per_token
        output_cost = log.output_tokens * pricing.output_price_per_token
        total_cost = input_cost + output_cost

        # Update log with costs
        log.input_cost = input_cost
        log.output_cost = output_cost
        log.total_cost = total_cost

        # Deduct from wallet and create transaction
        with transaction.atomic():
            if total_cost != 0:
                wallet_transaction = update_api_wallet(user=user, transaction_type=APIWalletTransaction.API_CHARGE, amount=total_cost,
                                                       description=f"API call to {endpoint}")

                # Link to API log
                log.wallet_transaction = wallet_transaction
            log.save()


def _los_subscription_usage(user: get_user_model(), endpoint: str):
    log = SubscriptionUsageLog(
        user=user,
        endpoint=endpoint,
        input_tokens=0,
        output_tokens=0,
        status=0
    )

    try:
        yield log
    except Exception as e:
        print('exception log: ', e)
        log.response_data = {'error': str(e)}
        log.status = 500
        raise
    finally:
        total_tokens = 0
        if log.input_tokens is not None and log.output_tokens is not None:
            total_tokens = log.input_tokens + log.output_tokens
        if total_tokens == 0:
            log.save()
        else:
            with transaction.atomic():
                now = datetime.now().date()
                remaining = total_tokens

                # Fetch eligible allocations ordered by soonest expiry
                allocations = SubscriptionTokenAllocation.objects.select_for_update().filter(
                    user=user,
                    tokens_used__lt=F('tokens_granted')
                ).filter(
                    Q(expires_at__isnull=True) | Q(expires_at__gte=now)
                ).order_by('expires_at')

                for allocation in allocations:
                    available = allocation.tokens_granted - allocation.tokens_used
                    to_deduct = min(available, remaining)

                    # Update allocation
                    allocation.tokens_used = F('tokens_used') + to_deduct
                    allocation.save(update_fields=['tokens_used'])

                    # Create token transaction
                    SubscriptionTokenTransaction.objects.create(
                        allocation=allocation,
                        usage_log=log,
                        tokens=to_deduct,
                        transaction_type=SubscriptionTokenTransaction.API_CHARGE,
                        description=f"API call to {endpoint}"
                    )

                    remaining -= to_deduct
                    if remaining <= 0:
                        break

                if remaining > 0:
                    raise Exception(f"Insufficient tokens: required {total_tokens}, short by {remaining}")

                log.save()

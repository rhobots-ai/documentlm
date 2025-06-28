from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from billing.services.razorpay_service import RazorpayService


def _parse_unix_timestamp(unix_timestamp) -> datetime | None:
    if unix_timestamp is None:
        return None
    return timezone.make_aware(datetime.fromtimestamp(unix_timestamp))


def get_subscription(user: get_user_model()):
    from billing.models import Subscription
    return Subscription.objects.filter(user=user).order_by('-created_at').first()


def disable_all_active_token_allocations(user):
    from billing.models import SubscriptionTokenAllocation
    SubscriptionTokenAllocation.objects.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=datetime.now().date()),
        user=user
    ).update(is_deallocated=True)


def create_free_plan_allocation(user):
    today = datetime.now().date()
    from billing.models import SubscriptionTokenAllocation
    source = SubscriptionTokenAllocation.SourceChoices.FREE_DAILY

    # Check if today's allocation already exists
    exists = SubscriptionTokenAllocation.objects.filter(
        user=user,
        source=source,
        expires_at=today
    ).exists()

    if not exists:
        SubscriptionTokenAllocation.objects.create(
            user=user,
            source=source,
            tokens_granted=150000,
            expires_at=today
        )


def refresh_subscription(subscription):
    from billing.models import SubscriptionInvoice, SubscriptionTokenAllocation, SubscriptionPlan

    razorpay_service = RazorpayService()
    razorpay_subscription = razorpay_service.get_subscription(subscription.gateway_subscription_id)
    subscription_invoices = razorpay_service.get_subscription_invoices(subscription.gateway_subscription_id)

    subscription_plan = SubscriptionPlan.objects.get(gateway_plan_id=razorpay_subscription['plan_id'])

    old_status = subscription.status
    new_status = razorpay_subscription.get('status', old_status)
    is_status_downgraded = old_status == 'active' and new_status in ['pending', 'halted', 'paused', 'cancelled', 'completed', 'expired']

    # Update subscription base info
    subscription.plan = subscription_plan
    subscription.status = new_status
    subscription.start_at = _parse_unix_timestamp(razorpay_subscription.get('start_at')) or subscription.start_at
    subscription.end_at = _parse_unix_timestamp(razorpay_subscription.get('end_at')) or subscription.end_at
    subscription.current_start = _parse_unix_timestamp(razorpay_subscription.get('current_start')) or subscription.current_start
    subscription.current_end = _parse_unix_timestamp(razorpay_subscription.get('current_end')) or subscription.current_end
    subscription.total_count = razorpay_subscription.get('total_count', subscription.total_count)
    subscription.remaining_count = razorpay_subscription.get('remaining_count', subscription.remaining_count)
    subscription.paid_count = razorpay_subscription.get('paid_count', subscription.paid_count)
    subscription.charge_at = _parse_unix_timestamp(razorpay_subscription.get('charge_at')) or subscription.charge_at
    subscription.has_scheduled_changes = razorpay_subscription.get('has_scheduled_changes', subscription.has_scheduled_changes)
    subscription.change_scheduled_at = _parse_unix_timestamp(razorpay_subscription.get('change_scheduled_at')) or subscription.change_scheduled_at
    subscription.save()

    # Downgrade logic
    if is_status_downgraded:
        disable_all_active_token_allocations(subscription.user)
        create_free_plan_allocation(subscription.user)
        return subscription

    for invoice_data in subscription_invoices:
        payment_id = invoice_data.get('payment_id')
        invoice_id = invoice_data.get('id')
        if not payment_id or not invoice_id:
            continue

        if SubscriptionInvoice.objects.filter(payment_id=payment_id).exists():
            continue  # Already processed

        with transaction.atomic():
            # Create invoice record
            invoice = SubscriptionInvoice.objects.create(
                subscription=subscription,
                plan=subscription.plan,
                amount=int(invoice_data.get('amount', 0)),
                currency=invoice_data.get('currency', 'USD'),
                status=invoice_data.get('status'),
                order_id=invoice_data.get('order_id'),
                payment_id=payment_id,
                invoice_id=invoice_id,
                issued_at=_parse_unix_timestamp(invoice_data.get('issued_at')),
                paid_at=_parse_unix_timestamp(invoice_data.get('paid_at')),
                billing_start=_parse_unix_timestamp(invoice_data.get('billing_start')),
                billing_end=_parse_unix_timestamp(invoice_data.get('billing_end')),
                gateway_short_url=invoice_data.get('short_url'),
                international=invoice_data.get('international'),
                method=invoice_data.get('method'),
                amount_refunded=int(invoice_data.get('amount_refunded', 0)) if invoice_data.get('amount_refunded') else None,
                refund_status=invoice_data.get('refund_status'),
                fee=int(invoice_data.get('fee', 0)) if invoice_data.get('fee') else None,
                tax=int(invoice_data.get('tax', 0)) if invoice_data.get('tax') else None,
            )

            disable_all_active_token_allocations(subscription.user)

            if subscription_plan.interval == 'yearly':
                expires_at = subscription.current_start + relativedelta(months=1)
            else:
                expires_at = subscription.current_end

            SubscriptionTokenAllocation.objects.create(
                user=subscription.user,
                source=SubscriptionTokenAllocation.SourceChoices.SUBSCRIPTION_PURCHASE,
                tokens_granted=subscription_plan.tokens,
                invoice=invoice,
                expires_at=expires_at.date()
            )

    return subscription

from django.db import models

from billing.enums import PaymentStatus
from billing.models import Subscription, SubscriptionPlan
from config.abstract_models import TimeStampedUUIDModel


class SubscriptionInvoice(TimeStampedUUIDModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issues'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('deleted', 'Deleted')
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='+')
    amount = models.IntegerField()
    currency = models.CharField(max_length=5, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    order_id = models.CharField(max_length=20, null=True, blank=True)
    payment_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    invoice_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    issued_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    billing_start = models.DateTimeField(null=True, blank=True)
    billing_end = models.DateTimeField(null=True, blank=True)
    gateway_short_url = models.URLField(blank=True, null=True)
    international = models.BooleanField(null=True, blank=True)
    method = models.CharField(max_length=20, null=True, blank=True)
    amount_refunded = models.IntegerField(null=True, blank=True)
    refund_status = models.CharField(max_length=20, null=True, blank=True)
    fee = models.IntegerField(null=True, blank=True)
    tax = models.IntegerField(null=True, blank=True)

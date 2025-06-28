from django.contrib.auth import get_user_model
from django.db import models

from billing.models import SubscriptionPlan
from config.abstract_models import TimeStampedUUIDModel


class Subscription(TimeStampedUUIDModel):
    """
    Tracks user subscriptions with Razorpay
    """
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('authenticated', 'Authenticated'),
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('halted', 'Halted'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    gateway_subscription_id = models.CharField(max_length=100, unique=True)
    gateway_short_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    charge_at = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    current_start = models.DateTimeField(null=True, blank=True)
    current_end = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    total_count = models.PositiveIntegerField(default=0)
    remaining_count = models.PositiveIntegerField(default=0)
    paid_count = models.PositiveIntegerField(default=0)
    notes = models.JSONField(default=dict, blank=True)
    has_scheduled_changes = models.BooleanField(default=False)
    change_scheduled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"

    @property
    def is_active(self):
        return self.status == 'active'

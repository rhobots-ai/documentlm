from django.db import models

from config.abstract_models import TimeStampedUUIDModel


class SubscriptionPlan(TimeStampedUUIDModel):
    """
    Represents a subscription plan in Payment Gateway
    """
    INTERVAL_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'),
    ]

    name = models.CharField(max_length=100)
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES)
    description = models.TextField(blank=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default='USD')
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    gateway_plan_id = models.CharField(max_length=100, unique=True)
    tokens = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gateway} - {self.name} ({self.get_interval_display()})"

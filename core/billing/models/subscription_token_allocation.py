from django.contrib.auth import get_user_model
from django.db import models

from config.abstract_models import TimeStampedUUIDModel


class SubscriptionTokenAllocation(TimeStampedUUIDModel):
    class SourceChoices(models.TextChoices):
        FREE_DAILY = 'free_daily', 'Free Daily Allocation'
        SUBSCRIPTION_PURCHASE = 'subscription_purchase', 'Subscription Purchase'
        ADMIN_GRANT = 'admin_grant', 'Admin Grant'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='token_allocations')
    source = models.CharField(max_length=50, choices=SourceChoices.choices)
    tokens_granted = models.BigIntegerField()
    tokens_used = models.BigIntegerField(default=0)
    expires_at = models.DateField(null=True, blank=True)
    invoice = models.OneToOneField('SubscriptionInvoice', null=True, blank=True, on_delete=models.CASCADE)
    is_deallocated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    @property
    def tokens_remaining(self):
        return max(0, self.tokens_granted - self.tokens_used)

    def __str__(self):
        return f"{self.user.email} - {self.get_source_display()} - Remaining: {self.tokens_remaining}"


class SubscriptionTokenTransaction(TimeStampedUUIDModel):
    DEPOSIT = 'deposit'
    API_CHARGE = 'api_charge'

    TRANSACTION_TYPES = (
        (DEPOSIT, 'Deposit'),
        (API_CHARGE, 'API Charge')
    )

    allocation = models.ForeignKey(SubscriptionTokenAllocation, on_delete=models.CASCADE, related_name='transactions')
    usage_log = models.ForeignKey('SubscriptionUsageLog', on_delete=models.CASCADE, related_name='transactions')
    tokens = models.BigIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.allocation.user.email} - {self.transaction_type} - {self.tokens}"

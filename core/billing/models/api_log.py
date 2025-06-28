from django.contrib.auth import get_user_model
from django.db import models

from billing.models import APIWalletTransaction
from config.abstract_models import TimeStampedUUIDModel


class APILog(TimeStampedUUIDModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='api_usage')
    endpoint = models.CharField(max_length=200)
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    input_cost = models.DecimalField(max_digits=20, decimal_places=8)
    output_cost = models.DecimalField(max_digits=20, decimal_places=8)
    total_cost = models.DecimalField(max_digits=20, decimal_places=8)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    error_data = models.JSONField(blank=True, null=True)
    status = models.PositiveIntegerField(default=0)
    wallet_transaction = models.OneToOneField(
        APIWalletTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='api_log'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.endpoint} - {self.total_cost}"

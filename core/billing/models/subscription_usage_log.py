from django.contrib.auth import get_user_model
from django.db import models

from config.abstract_models import TimeStampedUUIDModel


class SubscriptionUsageLog(TimeStampedUUIDModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='token_usage_logs')
    endpoint = models.CharField(max_length=200)
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    error_data = models.JSONField(blank=True, null=True)
    status = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        total = self.input_tokens + self.output_tokens
        return f"{self.user.email} - {self.endpoint} - {total}"

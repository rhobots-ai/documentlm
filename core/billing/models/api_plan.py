from django.db import models

from config.abstract_models import TimeStampedUUIDModel


class APIPlan(TimeStampedUUIDModel):
    """Base pricing plan that can be customized per user"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_input_price_per_token = models.DecimalField(max_digits=10, decimal_places=8)
    default_output_price_per_token = models.DecimalField(max_digits=10, decimal_places=8)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from django.contrib.auth import get_user_model
from django.db import models

from billing.models import APIPlan
from config.abstract_models import TimeStampedUUIDModel


class APIUserPricing(TimeStampedUUIDModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='pricing')
    base_plan = models.ForeignKey(APIPlan, on_delete=models.PROTECT)
    custom_input_price_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True
    )
    custom_output_price_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True
    )
    effective_from = models.DateTimeField(auto_now_add=True)

    @property
    def input_price_per_token(self):
        return self.custom_input_price_per_token or self.base_plan.default_input_price_per_token

    @property
    def output_price_per_token(self):
        return self.custom_output_price_per_token or self.base_plan.default_output_price_per_token

    def __str__(self):
        return f"Custom pricing for {self.user.email}"

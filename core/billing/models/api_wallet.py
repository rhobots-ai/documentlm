from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Organization
from config.abstract_models import TimeStampedUUIDModel


class APIWallet(TimeStampedUUIDModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='api_wallet')
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name="wallet"
    )
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"{self.user.email} - {self.balance} {self.currency}"


class APIWalletTransaction(TimeStampedUUIDModel):
    DEPOSIT = 'deposit'
    API_CHARGE = 'api_charge'

    TRANSACTION_TYPES = (
        (DEPOSIT, 'Deposit'),
        (API_CHARGE, 'API Charge')
    )

    wallet = models.ForeignKey(APIWallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wallet.user.email} - {self.transaction_type} - {self.amount}"

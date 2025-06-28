from django.contrib.auth import get_user_model
from django.db import models, transaction

from billing.enums import PaymentStatus
from billing.models import APIWalletTransaction
from billing.services import RazorpayService, update_api_wallet
from config.abstract_models import TimeStampedUUIDModel


class APIPayment(TimeStampedUUIDModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    amount = models.IntegerField()
    currency = models.CharField(max_length=5, default='USD')
    status = models.IntegerField(choices=PaymentStatus.choices())
    order_id = models.CharField(max_length=20, null=True, blank=True)
    payment_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    international = models.BooleanField(null=True, blank=True)
    method = models.CharField(max_length=20, null=True, blank=True)
    amount_refunded = models.IntegerField(null=True, blank=True)
    refund_status = models.CharField(max_length=20, null=True, blank=True)
    captured = models.BooleanField(default=False)
    fee = models.IntegerField(null=True, blank=True)
    tax = models.IntegerField(null=True, blank=True)
    wallet_transaction = models.OneToOneField(
        APIWalletTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment'
    )

    def create_order(self):
        if self.order_id is not None:
            raise Exception('Order is already created for this transaction.')
        payment_gateway = RazorpayService()
        order_id = payment_gateway.create_order(receipt_id=self.id, amount=int(self.amount), currency=self.currency)
        self.order_id = order_id
        self.save()

    def update_status(self, payment_id, signature):
        if self.status == PaymentStatus.SUCCESS or self.status == PaymentStatus.FAILED:
            return False

        with transaction.atomic():
            payment_gateway = RazorpayService()

            payment_gateway.verify_payment_signature(order_id=self.order_id, payment_id=payment_id, signature=signature)
            payments = payment_gateway.get_payments_by_order(self.order_id)
            successful_payments = list(filter(lambda p: p['status'] == 'captured', payments['items']))
            successful_payment = successful_payments[0] if len(successful_payments) != 0 else None
            if successful_payment is not None:
                self.payment_id = payment_id
                self.captured = True
                self.status = PaymentStatus.SUCCESS
                self.international = successful_payment['international']
                self.method = successful_payment['method']
                self.fee = successful_payment['fee']
                self.tax = successful_payment['tax']
                self.save()

                # update wallet
                self.wallet_transaction = update_api_wallet(user=self.user, transaction_type=APIWalletTransaction.DEPOSIT, amount=self.amount / 100.0)
                self.save()
            else:
                raise Exception('Payment was not successful. Please try again.')

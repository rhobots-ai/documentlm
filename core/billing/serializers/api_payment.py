from rest_framework import serializers

from billing.models import APIPayment
from config import settings


class APIPaymentSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    def get_key(self, obj):
        return settings.RAZORPAY_KEY

    class Meta:
        model = APIPayment
        fields = '__all__'
        read_only_fields = ['user', 'order_id', 'payment_id', 'captured', 'status', 'wallet_transaction']

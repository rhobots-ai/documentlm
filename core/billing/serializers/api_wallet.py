from rest_framework import serializers

from billing.models import APIWallet, APIWalletTransaction


class APIWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIWallet
        fields = ['id', 'balance', 'currency', 'created_at', 'updated_at']


class APIWalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIWalletTransaction
        fields = ['id', 'amount', 'transaction_type', 'description', 'created_at']

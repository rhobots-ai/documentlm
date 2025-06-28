# wallets/views.py
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from billing.models import APIWallet, APIWalletTransaction
from billing.serializers import APIWalletSerializer, APIWalletTransactionSerializer


@extend_schema(exclude=True)
class APIWalletDetailView(generics.RetrieveAPIView):
    serializer_class = APIWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return APIWallet.objects.get(organization=self.request.organization)


@extend_schema(exclude=True)
class APIWalletTransactionListView(generics.ListAPIView):
    serializer_class = APIWalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet_id = self.kwargs.get('wallet_id')
        return APIWalletTransaction.objects.filter(wallet_id=wallet_id, wallet__organization=self.request.organization)

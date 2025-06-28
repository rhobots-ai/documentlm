from decimal import Decimal

from django.contrib.auth import get_user_model

from billing.models import APIWallet, APIWalletTransaction


def update_api_wallet(user: get_user_model(), transaction_type: str, amount: float, description=None) -> APIWalletTransaction:
    wallet = APIWallet.objects.select_for_update().get(user=user)
    if transaction_type == APIWalletTransaction.DEPOSIT:
        wallet.balance += Decimal(str(amount))
    else:
        wallet.balance -= Decimal(str(amount))
    wallet.save()

    # Create wallet transaction
    wallet_transaction = APIWalletTransaction.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type=transaction_type,
        description=description if description is not None else transaction_type
    )

    return wallet_transaction

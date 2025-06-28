from django.urls import path, include
from rest_framework import routers

from billing import views

router = routers.DefaultRouter()
router.register(r'payments', views.APIPaymentViewSet, basename='payments')
router.register(r'subscription-plans', views.SubscriptionPlanViewSet, basename='subscription-plans')
router.register(r'subscription', views.SubscriptionViewSet, basename='subscription')


urlpatterns = [
    path('', include(router.urls)),
    path('wallet/', views.APIWalletDetailView.as_view(), name='wallet-detail'),
    path('wallets/<uuid:wallet_id>/transactions/', views.APIWalletTransactionListView.as_view(), name='wallet-transactions'),
]

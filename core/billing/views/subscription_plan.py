from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

from billing.models import SubscriptionPlan
from billing.serializers import SubscriptionPlanSerializer


@extend_schema(exclude=True)
class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only view for listing and retrieving subscription plans.
    """
    queryset = SubscriptionPlan.objects.filter(is_active=True).order_by('amount')
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

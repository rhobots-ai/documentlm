from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from billing.models import Subscription, SubscriptionPlan
from billing.serializers import SubscriptionSerializer
from billing.services import RazorpayService, get_subscription, refresh_subscription
from billing.utils import get_token_usage


@extend_schema(exclude=True)
class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        subscription = get_subscription(request.user)
        if not subscription:
            return Response(None, status=200)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='usage')
    def usage(self, request):
        user = request.user
        token_usage = get_token_usage(user)

        return Response(token_usage)

    @action(detail=False, methods=['get'], url_path='refresh')
    def refresh(self, request):
        subscription = get_subscription(request.user)
        if not subscription:
            return Response(None, status=200)
        subscription = refresh_subscription(subscription)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='new')
    def new(self, request, *args, **kwargs):
        user = request.user
        plan_id = request.data.get("plan_id")
        plan = get_object_or_404(SubscriptionPlan, gateway_plan_id=plan_id, is_active=True)

        existing_sub = get_subscription(request.user)
        razorpay_service = RazorpayService()

        if existing_sub:
            if existing_sub.plan == plan:
                # Same plan — return existing subscription
                serializer = SubscriptionSerializer(existing_sub)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                is_upgraded = plan.amount > existing_sub.plan.amount
                razorpay_service.update_subscription(existing_sub.gateway_subscription_id, {
                    'plan_id': plan_id,
                    'schedule_change_at': 'now' if is_upgraded else 'cycle_end'
                })
                subscription = refresh_subscription(existing_sub)
                serializer = SubscriptionSerializer(subscription)
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Prepare Razorpay subscription data
        # Call Razorpay to create the subscription
        rp_sub = razorpay_service.create_subscription(plan_id)

        # Create a local subscription object
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            gateway_subscription_id=rp_sub["id"],
            gateway_short_url=rp_sub.get("short_url"),
            status=rp_sub.get("status", "created"),
            total_count=rp_sub.get("total_count", 0),
            remaining_count=rp_sub.get("remaining_count", 0),
            paid_count=rp_sub.get("paid_count", 0),
            quantity=rp_sub.get("quantity", 1),
            start_at=timezone.datetime.fromtimestamp(rp_sub.get("start_at", 0)) if rp_sub.get("start_at") else None,
            end_at=timezone.datetime.fromtimestamp(rp_sub.get("end_at", 0)) if rp_sub.get("end_at") else None,
        )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

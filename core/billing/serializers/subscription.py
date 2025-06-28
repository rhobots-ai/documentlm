from rest_framework import serializers

from billing.models import Subscription, SubscriptionPlan


class SubscriptionPlanSerializerSummary(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'name', 'interval', 'amount')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializerSummary()

    class Meta:
        model = Subscription
        fields = '__all__'

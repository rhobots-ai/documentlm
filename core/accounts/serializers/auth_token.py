# serializers.py
from rest_framework import serializers

from accounts.models import AuthToken


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ('digest', 'name', 'token_key', 'created', 'expiry', 'user')

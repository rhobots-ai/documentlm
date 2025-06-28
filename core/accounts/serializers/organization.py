# serializers.py
from rest_framework import serializers

from accounts.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'created_by', 'created_at', 'updated_at', 'metadata']
        read_only_fields = ['id', 'slug', 'metadata', 'created_by', 'created_at', 'updated_at']

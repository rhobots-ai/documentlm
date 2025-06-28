from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Space, SpaceMembership, DataSource, Conversation, SpaceTag


class SpaceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name']


class SpaceMembershipSerializer(serializers.ModelSerializer):
    user = SpaceUserSerializer()

    class Meta:
        model = SpaceMembership
        fields = ['user', 'is_admin', 'joined_at']


class SpaceDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'title', 'size', 'file', 'status', 'created_at']


class SpaceConversationSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'message_count', 'created_by', 'created_at', 'last_message_at']

    def get_created_by(self, obj) -> str:
        return obj.created_by.get_full_name()

    def get_message_count(self, obj) -> int:
        return obj.messages.count()


class SpaceSerializer(serializers.ModelSerializer):
    members = SpaceMembershipSerializer(source='spacemembership_set', many=True, read_only=True)
    data_sources = SpaceDataSourceSerializer(many=True, read_only=True)
    conversations = SpaceConversationSerializer(many=True, read_only=True)

    class Meta:
        model = Space
        fields = [
            'id', 'name', 'slug', 'icon', 'description', 'is_public', 'created_at', 'updated_at',
            'members', 'data_sources', 'conversations'
        ]
        read_only_fields = ['slug', 'created_at']

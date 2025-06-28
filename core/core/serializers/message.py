from rest_framework import serializers

from core.models import Message


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    conversation = serializers.UUIDField()
    sender = serializers.ReadOnlyField(source='sender.email')
    mindmap = serializers.JSONField(required=False)
    citation = serializers.JSONField(required=False)
    raw_content = serializers.CharField(required=False, allow_blank=True)

    # def get_id(self, obj):
    #     return str(obj.id)

    class Meta:
        model = Message
        fields = [
            'id',
            'conversation',
            'sender',
            'role',
            'content',
            'raw_content',
            'mindmap',
            'citation',
            'citation_type',
            'is_upvote',
            'created_at',
        ]
        read_only_fields = ['sender', 'conversation', 'role', 'content', 'raw_content', 'citation', 'citation_type', 'mindmap', 'created_at']

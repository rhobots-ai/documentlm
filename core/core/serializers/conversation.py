from rest_framework import serializers

from core.models import DataSource, Conversation, Message, ConversationNote, Space


class ConversationDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'title', 'file', 'status']


class ConversationMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'reason_content', 'conversation_id', 'mindmap', 'citation', 'citation_type', 'role', 'sender', 'is_upvote', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    space = serializers.PrimaryKeyRelatedField(
        queryset=Conversation._meta.get_field('space').related_model.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Conversation
        fields = [
            'id',
            'name',
            'space',
            'is_public',
            'created_by',
            'created_at',
            'last_message_at'
        ]
        read_only_fields = ['created_by', 'created_at']


class ConversationNoteSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        required=True
    )

    class Meta:
        model = ConversationNote
        fields = ['id', 'conversation', 'type', 'content', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class ConversationSpaceSerializer(serializers.ModelSerializer):
    data_sources = ConversationDataSourceSerializer(many=True, read_only=True)

    class Meta:
        model = Space
        fields = [
            'id', 'name', 'slug', 'icon', 'description', 'is_public', 'created_at', 'updated_at', 'data_sources'
        ]
        read_only_fields = ['slug', 'created_at', 'data_sources']


class ConversationSerializer(serializers.ModelSerializer):
    data_sources = ConversationDataSourceSerializer(many=True, read_only=True)
    data_source_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
        help_text="List of DataSource UUIDs to associate with this conversation"
    )
    messages = ConversationMessageSerializer(many=True, read_only=True)
    notes = ConversationNoteSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField()
    space = ConversationSpaceSerializer(read_only=True)
    space_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'name',
            'space',
            'space_id',
            'is_public',
            'data_sources',
            'data_source_ids',
            'messages',
            'notes',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['data_sources', 'space', 'messages', 'notes', 'created_by', 'created_at']

    def create(self, validated_data):
        data_source_ids = validated_data.pop('data_source_ids', [])
        conversation = super().create(validated_data)
        if data_source_ids:
            conversation.data_sources.set(data_source_ids)
        return conversation

    def get_created_by(self, obj) -> str:
        return obj.created_by.get_full_name()

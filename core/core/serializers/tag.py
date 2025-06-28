from rest_framework import serializers
from core.models import Tag, SpaceTag
from core.serializers import SpaceSerializer


class TagSerializer(serializers.ModelSerializer):
    spaces = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.email')
    spaces_to_tag = serializers.ListField(write_only=True)
    spaces_to_untag = serializers.ListField(write_only=True)

    def get_spaces(self, obj):
        spaces = [space_tag.space for space_tag in obj.spaces.all()]
        serializer = SpaceSerializer(spaces, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        spaces_to_tag = validated_data.pop('spaces_to_tag', None)
        spaces_to_untag = validated_data.pop('spaces_to_untag', None)

        print('spaces_to_tag: ', spaces_to_tag)

        # Update space fields
        tag = super().update(instance, validated_data)

        # Handle tags if provided
        if spaces_to_tag is not None:
            for space in spaces_to_tag:
                SpaceTag.objects.create(space_id=space, tag=tag)

        if spaces_to_untag is not None:
            SpaceTag.objects.filter(space_id__in=spaces_to_untag, tag=tag).delete()

        return tag

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'user',
            'parent_id',
            'organization',
            'created_at',
            'spaces',
            'spaces_to_tag',
            'spaces_to_untag'
        ]
        read_only_fields = ['user', 'organization', 'created_at']

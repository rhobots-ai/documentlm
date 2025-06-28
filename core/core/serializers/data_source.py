from rest_framework import serializers

from core.models import DataSource


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class DataSourceSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = DataSource
        fields = [
            'id',
            'title',
            'data_type',
            'file',
            'status',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['status', 'created_by', 'created_at']

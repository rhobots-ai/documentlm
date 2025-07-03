import os

from django.conf import settings
from django.db import models

from config.abstract_models import TimeStampedUUIDModel


def user_directory_path(instance, filename):
    file_uuid = str(instance.id)
    file_extension = os.path.splitext(filename)[1]
    return os.path.join(str(instance.created_by.id), f"{file_uuid}{file_extension}")


class DataSource(TimeStampedUUIDModel):
    DATA_TYPE_CHOICES = [
        ('document', 'Document'),
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('url', 'Web URL'),
    ]

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('indexed', 'Indexed'),
        ('errored', 'Errored'),
    ]

    title = models.CharField(max_length=255)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)
    file = models.FileField(upload_to=user_directory_path, max_length=500, blank=True, null=True)
    size = models.BigIntegerField(null=True, blank=True)  # Size in bytes
    data = models.JSONField(null=True, blank=True)  # For extracted text, metadata, etc.
    is_created_via_platform = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    spaces = models.ManyToManyField('core.Space', blank=True, related_name='data_sources')

    def __str__(self):
        return f"{self.title} ({self.data_type})"

    def _validate_status(self, new_status):
        valid_statuses = dict(self.STATUS_CHOICES).keys()
        if new_status not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

    def start_indexing(self):
        if self.status == 'indexed':
            raise Exception('Already indexed.')

        from core.tasks import index_data_source
        index_data_source.delay(str(self.id), str(self.created_by_id), '/api/data-sources/', False)


    def update_status(self, new_status):
        self._validate_status(new_status)
        self.status = new_status
        self.save()


class DataSourceIndex(TimeStampedUUIDModel):
    RELATION_TYPE_CHOICES = [
        ('document', 'Document'),
        ('vector', 'Vector'),
    ]

    source = models.ForeignKey('core.DataSource', on_delete=models.CASCADE, related_name='indices')
    target_id = models.UUIDField()
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.relation_type} index for {self.source.title}"

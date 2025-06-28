from django.conf import settings
from django.db import models

from config.abstract_models import TimeStampedUUIDModel


class FileGroup(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    data = models.JSONField(null=True, blank=True)  # For extracted text, metadata, etc.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

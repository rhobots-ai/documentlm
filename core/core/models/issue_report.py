from django.db import models

from config import settings
from config.abstract_models import TimeStampedUUIDModel


class IssueReport(TimeStampedUUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issues = models.JSONField()
    chat = models.JSONField()
    settings = models.JSONField()

    def __str__(self):
        return self.user.email

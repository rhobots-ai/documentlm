from django.db import models

from config.abstract_models import TimeStampedUUIDModel


class Reranking(TimeStampedUUIDModel):
    name = models.TextField(max_length=20)
    spec = models.JSONField()
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

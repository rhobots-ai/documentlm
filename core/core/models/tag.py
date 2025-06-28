from django.conf import settings
from django.db import models

from config.abstract_models import TimeStampedUUIDModel
from core.models import Space, DataSource


class Tag(TimeStampedUUIDModel):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')
    organization = models.ForeignKey(
        'accounts.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tags'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name


class SpaceTag(TimeStampedUUIDModel):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='spaces')


class DataSourceTag(TimeStampedUUIDModel):
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

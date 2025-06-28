from django.db import models


class Index(models.Model):
    name = models.TextField(max_length=20, unique=True)
    index_type = models.TextField(max_length=200)
    config = models.JSONField(default=list)

    def __str__(self):
        return self.name

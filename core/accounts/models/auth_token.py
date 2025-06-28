from django.db import models
from knox.models import AbstractAuthToken


class AuthToken(AbstractAuthToken):
    name = models.CharField(max_length=20, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

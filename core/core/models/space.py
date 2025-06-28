from django.db import models
from django.utils.text import slugify

from accounts.models import Organization
from config import settings
from config.abstract_models import OrgTimeStampedUUIDModel, TimeStampedUUIDModel


class Space(OrgTimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_public = models.BooleanField(default=False)
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="spaces"
    )
    is_created_via_platform = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Space.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SpaceMembership(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'space')


class SpaceInvitation(TimeStampedUUIDModel):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_sent')
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_received')
    accepted = models.BooleanField(default=False)

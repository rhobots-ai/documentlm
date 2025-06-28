from django.db import models

from config import settings
from config.abstract_models import TimeStampedUUIDModel


class Conversation(TimeStampedUUIDModel):
    space = models.ForeignKey(
        'Space',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    data_sources = models.ManyToManyField('DataSource', blank=True, related_name='conversations')
    last_message_at = models.DateTimeField(auto_now=True)
    is_created_via_platform = models.BooleanField(default=False)


class ConversationNote(TimeStampedUUIDModel):
    NOTE_TYPE_CHOICES = [
        ('summary', 'Summary'),
        ('insight', 'Study Guide'),
        ('action', 'FAQs'),
        ('bullet', 'Bullet Points'),
        ('note', 'Note'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    type = models.CharField(max_length=50, choices=NOTE_TYPE_CHOICES, default='note')
    content = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversation_notes'
    )

    def __str__(self):
        return f"{self.get_type_display()} - {self.content[:30]}"

    class Meta:
        ordering = ['-created_at']

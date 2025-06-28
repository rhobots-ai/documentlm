from django.db import models

from config import settings
from config.abstract_models import TimeStampedUUIDModel


class Message(TimeStampedUUIDModel):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('agent', 'Agent'),
        ('system', 'System'),
    ]
    CITATION_TYPE_CHOICES = [
        ('highlight', 'Highlight'),
        ('inline', 'Inline')
    ]
    REASONING_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('complex', 'Complex')
    ]
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    raw_content = models.TextField(blank=True, null=True)
    citation = models.JSONField(blank=True, null=True)
    citation_type = models.CharField(max_length=20, choices=CITATION_TYPE_CHOICES, default='highlight')
    reasoning_type = models.CharField(max_length=20, choices=REASONING_TYPE_CHOICES, default='highlight')
    reason_content = models.TextField(null=True, blank=True)
    mindmap = models.JSONField(blank=True, null=True)
    token_usage = models.JSONField(blank=True, null=True)
    input_tokens = models.IntegerField(blank=True, null=True)
    output_tokens = models.IntegerField(blank=True, null=True)
    is_upvote = models.BooleanField(null=True, blank=True)

    def __str__(self):
        sender_label = 'System' if self.role == 'system' else ('Agent' if self.role == 'agent' else self.sender.email if self.sender else 'Unknown')
        return f"{sender_label}: {self.content[:50]}"

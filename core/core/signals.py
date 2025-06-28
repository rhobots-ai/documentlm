from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Message


@receiver(post_save, sender=Message)
def update_conversation_timestamp(sender, instance, created, **kwargs):
    instance.conversation.last_message_at = instance.created_at
    instance.conversation.save()

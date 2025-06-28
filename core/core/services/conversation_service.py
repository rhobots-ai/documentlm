import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from accounts.models import User
from core.models import Conversation, Message
from core.types import Completion
from utils.text import clean_json


def create_or_update_conversation_with_data_source(created_by: User, data_sources, conversation_id: str | None, is_platform: bool):
    with transaction.atomic():
        if conversation_id is not None:
            try:
                conversation = Conversation.objects.get(pk=conversation_id, created_by=created_by)
            except ObjectDoesNotExist:
                raise ValueError("Conversation not found or access denied")
        else:
            conversation = Conversation.objects.create(
                name='New Conversation',
                created_by=created_by,
                is_public=False,
                is_created_via_platform=is_platform
            )

        conversation.data_sources.add(*data_sources)

    return conversation


def convert_square_brackets_to_html(text):
    """
    Convert square bracket-wrapped numbers (e.g., [1]) to HTML format (<a class="mark">1</a>).

    Args:
        text (str): Input text containing square bracket citations.

    Returns:
        str: Text with square brackets replaced by HTML tags.
    """
    # Use regular expression to find all [number] patterns and replace them
    converted_text = re.sub(
        r'\【(\d+)\】',
        r'<a class="mark" href="#mark-\1">\1</a>',
        text
    )
    return converted_text

def create_conversation_message(conversation: Conversation, role: str, content: str | None = None, completion: Completion | None = None,
                                sender: User | None = None, citation_type: str = 'highlight', reasoning_type: str = 'simple'):
    if completion is not None:
        chat_history = completion['chat_history']
        content = chat_history[-1][-1] if chat_history else ''
    token_usage = completion.get('token_usage', None) if completion is not None else None
    input_tokens = None
    output_tokens = None
    if token_usage is not None:
        input_tokens = token_usage['totals']['prompt_tokens']
        output_tokens = token_usage['totals']['completion_tokens']
    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        role=role,
        content=convert_square_brackets_to_html(content),
        mindmap=clean_json(completion.get('mindmap', None)) if completion is not None else None,
        token_usage=token_usage,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        citation=clean_json(completion.get('evidences', None)) if completion is not None else None,
        citation_type=citation_type,
        reasoning_type=reasoning_type,
        reason_content=completion.get('reason_content', None) if completion is not None else None
    )
    return message

from typing import List

import requests

from config import settings
from core.models import DataSource, Message


def _build_chat_history(messages: List[Message]) -> List[List[str]]:
    chat_history = []
    i = 0

    while i < len(messages) - 1:
        current_msg = messages[i]
        next_msg = messages[i + 1]

        if current_msg.role == 'user' and next_msg.role == 'agent':
            chat_history.append([current_msg.content, next_msg.content])
            i += 2
        else:
            # Skip malformed pairs or system messages
            i += 1

    return chat_history

class DCService:
    def __init__(self):
        self._base_url = settings.DEEPCITE_RAG_EP

    def delete_data_source(self, file_ids: list[str]):
        response = requests.post(
            f"{self._base_url}/documents/delete/",
            json={
                'file_ids': file_ids
            }
        )
        response.raise_for_status()
        return response

    def create_data_source(self, file_ids: list[str], user_id: str, stream: bool):
        response = requests.post(
            f"{self._base_url}/documents/upload/",
            json={
                'file_ids': file_ids,
                'user_id': user_id,
                'reindex': 'true',
                'stream': stream
            },
            headers={'Accept': 'text/event-stream'},
            stream=stream
        )
        response.raise_for_status()
        return response

    def chat_completion(self, user_id: str, sources: List[DataSource], user_message, chat_history: List[Message], stream: bool, citation: str = 'highlight', reasoning_type: str = 'simple'):
        first_selector_choices = [
            [ds.title, str(ds.id)] for ds in sources
        ]
        request_body = {
            "chat_input": {
                "text": user_message,
                "files": []
            },
            "is_conversation_flow": False,
            "chat_history": _build_chat_history(chat_history),
            "stream": stream,
            "user_id": user_id,
            "use_citation": citation,
            "first_selector_choices": first_selector_choices,
            "reasoning_type": reasoning_type
        }
        response = requests.post(
            f"{self._base_url}/chat/",
            json=request_body,
            stream=stream
        )
        response.raise_for_status()
        return response

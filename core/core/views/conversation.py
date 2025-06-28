import json
import uuid

import sseclient
from django.db.models import Prefetch
from django.http import StreamingHttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, inline_serializer, OpenApiExample, OpenApiResponse
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from billing.decorators import require_tokens
from billing.utils import log_usage
from config.renderers import SSERenderer
from core.models import Conversation, ConversationNote, Message
from core.serializers import ConversationSerializer, ConversationListSerializer, ConversationNoteSerializer, MessageSerializer
from core.services import DCService, create_conversation_message


@extend_schema_view(
    list=extend_schema(
        summary='List Conversations',
        description='Returns a paginated list of conversations, optionally filtered by query parameters.',
        responses={200: ConversationSerializer(many=True)}
    ),
    create=extend_schema(
        summary='Create Conversation',
        description='Creates a new conversation.',
        request=ConversationSerializer,
        responses={201: ConversationSerializer}
    ),
    retrieve=extend_schema(
        summary='Get Conversation',
        description='Retrieve a conversation by ID.',
        responses={200: ConversationSerializer}
    ),
    completion=extend_schema(
        summary="Chat Completion",
        description="Sends a user message and receives a model-generated response. Supports both streaming (SSE) and standard JSON.",
        request=inline_serializer(
            name='CompletionRequestSerializer',
            fields={
                'message': serializers.CharField(
                    required=True,
                    help_text="User's input message to the AI model"
                ),
                'citation': serializers.CharField(
                    default='highlight',
                    help_text="highlight or inline"
                )
            }
        ),
        parameters=[
            OpenApiParameter(
                name="stream",
                description="If set to true or if Accept header is 'text/event-stream', response will stream via SSE.",
                required=False,
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY
            )
        ],
        responses={
            200: OpenApiResponse(
                response=MessageSerializer,
                description="Standard response with AI reply (non-streaming)"
            ),
            206: OpenApiResponse(
                description="SSE streaming response. Events include: `thinking`, `chunk`, `complete`, `final`.",
                examples=[
                    OpenApiExample(
                        "SSE stream format",
                        value='event: chunk\ndata: "This is a streamed token."\n\n',
                        response_only=True
                    ),
                    OpenApiExample(
                        "Final message",
                        value='event: final\ndata: {"id": "uuid", "content": "..."}\n\n',
                        response_only=True
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request. 'message' field is required.",
                examples=[
                    OpenApiExample(
                        "Missing message",
                        value={"error": "Message is required."},
                        response_only=True
                    )
                ]
            )
        }
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(
        summary='Delete conversation',
        description='Deletes a conversation by ID.',
    )
)
@extend_schema(tags=["Conversation"])
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Conversation.objects.none()

    def get_queryset(self):
        # Prefetch messages ordered by created_at
        message_prefetch = Prefetch(
            'messages',
            queryset=Message.objects.order_by('created_at')
        )

        return Conversation.objects.filter(
            created_by=self.request.user,
            is_created_via_platform=self.request.is_platform
        ).order_by('-last_message_at').prefetch_related(message_prefetch)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, is_created_via_platform=self.request.is_platform)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ConversationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ConversationListSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="completion", renderer_classes=[SSERenderer, JSONRenderer])
    @require_tokens()
    def completion(self, request, pk=None):
        # Check Accept header if streaming is requested
        accept_header = request.META.get('HTTP_ACCEPT', '')
        stream = request.query_params.get("stream", "false").lower() == "true" or 'text/event-stream' in accept_header

        conversation = self.get_object()
        user_message = request.data.get("message")
        citation = request.data.get("citation", "highlight")
        reasoning_type = request.data.get("reasoning_type", "simple")

        if not user_message:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        create_conversation_message(conversation=conversation, role="user", content=user_message, sender=request.user)

        if conversation.space is not None:
            sources = conversation.space.data_sources.all()
        else:
            sources = conversation.data_sources.all()
        chat_history = list(conversation.messages.order_by("created_at"))

        dc_service = DCService()

        if stream:
            def event_stream():
                with log_usage(request.user, request.path, request.is_platform) as log:
                    async_response = dc_service.chat_completion(
                        user_id=str(request.user.id),
                        user_message=user_message,
                        sources=sources,
                        chat_history=chat_history,
                        stream=True,
                        citation=citation,
                        reasoning_type=reasoning_type
                    )
                    client = sseclient.SSEClient(async_response)
                    data = None
                    answer = ''
                    reason_content = ''
                    previous_answer_chunk = None
                    for event in client.events():
                        if event.event == 'heartbeat' or event.event == 'complete':
                            yield f"id: {str(uuid.uuid4())}\nevent: {event.event}\ndata: {event.data}\n\n"
                            if event.event == 'complete':
                                break
                        else:
                            data = json.loads(event.data)
                            chat_history_chunk = data['chat_history']
                            answer_chunk = chat_history_chunk[-1][-1] if chat_history_chunk else ''
                            if answer_chunk.lower().strip() == 'thinking ...':
                                ...
                            elif not (answer_chunk == '.' and previous_answer_chunk == '.'):
                                if event.event == 'thinking':
                                    reason_content += answer_chunk
                                    yield f"id: {str(uuid.uuid4())}\nevent: thinking\ndata: {json.dumps(answer_chunk)}\n\n"
                                else:
                                    answer += answer_chunk
                                    yield f"id: {str(uuid.uuid4())}\nevent: chunk\ndata: {json.dumps(answer_chunk)}\n\n"
                            previous_answer_chunk = answer_chunk
                    data['chat_history'][-1][-1] = answer
                    data['reason_content'] = reason_content
                    agent_message = create_conversation_message(conversation=conversation, role="agent", completion=data, sender=None, citation_type=citation, reasoning_type=reasoning_type)
                    response_message = MessageSerializer(agent_message).data

                    log.request_data = request.data
                    log.response_data = response_message
                    log.input_tokens = agent_message.input_tokens if agent_message.input_tokens else 0
                    log.output_tokens = agent_message.output_tokens if agent_message.output_tokens else 0
                    log.status = status.HTTP_200_OK

                    yield f"id: {str(uuid.uuid4())}\nevent: final\ndata: {json.dumps(response_message)}\n\n"

            response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
            response["Cache-Control"] = "no-cache"
            response["X-Accel-Buffering"] = "no"
            return response

        else:
            response = dc_service.chat_completion(
                user_id=str(request.user.id),
                user_message=user_message,
                sources=sources,
                chat_history=chat_history,
                stream=False,
                citation=citation,
                reasoning_type=reasoning_type
            )
            ai_message = create_conversation_message(conversation=conversation, role="agent", completion=response.json(), sender=None, citation_type=citation, reasoning_type=reasoning_type)
            return Response(MessageSerializer(ai_message).data, status=status.HTTP_200_OK)


@extend_schema(exclude=True)
class ConversationNoteViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    def get_queryset(self):
        return ConversationNote.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

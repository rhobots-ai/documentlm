from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from config.permissions import IsOrgMember
from core.models import Space, Conversation, DataSource
from core.serializers import SpaceSerializer


@extend_schema_view(
    list=extend_schema(
        summary='List Spaces',
        description='Returns a paginated list of spaces, optionally filtered by query parameters.',
        responses={200: SpaceSerializer(many=True)}
    ),
    create=extend_schema(
        summary='Create Space',
        description='Creates a new space.',
        request=SpaceSerializer,
        responses={201: SpaceSerializer}
    ),
    retrieve=extend_schema(
        summary='Get Space',
        description='Retrieve a space by ID.',
        responses={200: SpaceSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(
        summary='Delete Space',
        description='Deletes a space by ID.',
    )
)
@extend_schema(tags=["Space"])
class SpaceViewSet(viewsets.ModelViewSet):
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Space.objects.none()

    def get_permissions(self):
        if self.action == 'retrieve' or (self.action == 'list' and self.request.organization is not None):
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Space.objects.filter(
            is_created_via_platform=self.request.is_platform
        )
        conversation_queryset = Conversation.objects.prefetch_related('messages')
        if hasattr(self.request, 'organization') and self.request.organization is not None:
            queryset = queryset.filter(organization=self.request.organization)
        else:
            queryset = queryset.filter(created_by_user=self.request.user)

        if self.request.user:
            conversation_queryset = Conversation.objects.filter(created_by=self.request.user)
        return (
            queryset
            .prefetch_related(
                Prefetch(
                    'data_sources',
                    queryset=DataSource.objects.order_by('-created_at')
                ),
                Prefetch(
                    'conversations',
                    queryset=conversation_queryset.order_by('-last_message_at')
                )
            ).order_by('-created_at')
        )

    def perform_create(self, serializer):
        serializer.save(
            created_by_user=self.request.user,
            organization=self.request.organization,
            is_created_via_platform=self.request.is_platform
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

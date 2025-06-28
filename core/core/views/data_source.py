
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, inline_serializer
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response

from billing.decorators import require_tokens
from core.models import DataSource
from core.serializers import DataSourceSerializer, ConversationSerializer
from core.services import create_or_update_conversation_with_data_source, add_data_source_to_space
from core.services.data_source_service import create_data_source
from core.tasks import index_data_source


@extend_schema_view(
    list=extend_schema(
        summary='List Data Sources',
        description='Returns a list of data sources created by the authenticated user.'
    ),
    retrieve=extend_schema(
        summary='Retrieve Data Source',
        description='Fetch a single data source by ID.'
    ),
    new=extend_schema(
        summary='Create Data Source',
        description='Upload a file or provide a URL to create a new data source. Optionally associate it with a conversation.',
        request=inline_serializer(
            name='DataSourceUploadSerializer',
            fields={
                'file': serializers.FileField(
                    required=False,
                    help_text="The file to upload. This field is optional. If not provided, a URL must be given."
                ),
                'url': serializers.URLField(
                    required=False,
                    help_text="The URL to a resource. This field is optional. If not provided, a file must be uploaded."
                ),
                'conversation_id': serializers.UUIDField(
                    required=False,
                    help_text="The ID of the conversation to associate the data source with. This field is optional."
                ),
                'space_id': serializers.UUIDField(
                    required=False,
                    help_text="The ID of the space to associate the data source with. This field is optional."
                )
            }
        ),
        responses={
            201: OpenApiResponse(
                response=ConversationSerializer
            ),
            400: OpenApiTypes.OBJECT
        },
        methods=["POST"],
    ),
    create=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(
        summary='Delete data source',
        description='Deletes a data source by ID.',
    )
)
@extend_schema(tags=["Data Source"])
class DataSourceViewSet(viewsets.ModelViewSet):
    serializer_class = DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DataSource.objects.none()

    def get_queryset(self):
        return DataSource.objects.filter(created_by=self.request.user, is_created_via_platform=self.request.is_platform)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @require_tokens()
    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        url = request.data.get('url', None)

        # Validate at least one file or URL is provided
        if not files and url is None:
            return Response(
                {'error': 'No files or url provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation_id = request.data.get('conversation_id', None)
        space_id = request.data.get('space_id', None)

        data_sources = []
        try:
            # Create data sources for each file
            if files:
                for file in files:
                    data_source = create_data_source(
                        created_by=request.user,
                        is_platform=request.is_platform,
                        file=file,
                        url=None
                    )
                    data_sources.append(data_source)

            # Create data source for URL if provided
            if url:
                data_source = create_data_source(
                    created_by=request.user,
                    is_platform=request.is_platform,
                    file=None,
                    url=url
                )
                data_sources.append(data_source)

            # Add to space or conversation
            conversation = None
            if space_id is not None:
                add_data_source_to_space(
                    data_sources=data_sources,
                    space_id=space_id
                )
            else:
                conversation = create_or_update_conversation_with_data_source(
                    created_by=request.user,
                    data_sources=data_sources,
                    conversation_id=conversation_id,
                    is_platform=request.is_platform
                )

            # Start indexing jobs for each data source
            for data_source in data_sources:
                index_data_source.delay(
                    data_source_id=str(data_source.id),
                    user_id=str(request.user.id),
                    path=request.path,
                    is_platform=request.is_platform
                )

            return Response({
                'conversation': ConversationSerializer(conversation).data if conversation is not None else None,
                'message': f'{len(data_sources)} data source(s) created successfully.',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Message
from core.serializers import MessageSerializer


@extend_schema(exclude=True)
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return Message.objects.all()

    @action(detail=True, methods=['patch'], url_path='upvote')
    def upvote(self, request, pk=None):
        message = self.get_object()
        message.is_upvote = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='downvote')
    def downvote(self, request, pk=None):
        message = self.get_object()
        message.is_upvote = False
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    # Disable standard CRUD operations
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

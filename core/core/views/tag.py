from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from core.models import Tag
from core.serializers import TagSerializer

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

@extend_schema(exclude=True)
class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_permissions(self):
        if self.action == 'list' and hasattr(self.request, 'organization') and self.request.organization is not None:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if hasattr(self.request, 'organization') and self.request.organization is not None:
            return Tag.objects.filter(organization=self.request.organization).order_by('created_at')
        return Tag.objects.filter(user=self.request.user).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, organization=self.request.organization)

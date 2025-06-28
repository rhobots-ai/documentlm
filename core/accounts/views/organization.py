# views.py
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

from accounts.models import Organization, OrganizationMembership
from accounts.serializers import OrganizationSerializer
from accounts.services import AuthService


@extend_schema(exclude=True)
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        org = serializer.save(created_by=self.request.user)

        auth_service = AuthService()
        auth_org = auth_service.create_organization(
            name=org.name,
            slug=org.slug,
            created_by=self.request.user.identity_provider_id,
            private_metadata={
                'id': org.id
            }
        )
        org.identity_provider_id = auth_org['id']
        org.save(update_fields=["identity_provider_id"])

        OrganizationMembership.objects.create(
            user=self.request.user,
            organization=org,
            role='admin'
        )

    def get_queryset(self):
        if self.action == 'list':
            return Organization.objects.all()
        return Organization.objects.filter(members__user=self.request.user).distinct()

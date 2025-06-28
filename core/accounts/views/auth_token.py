from datetime import timedelta

from drf_spectacular.utils import extend_schema
from knox.models import get_token_model
from knox.views import LoginView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import AuthToken
from accounts.serializers import AuthTokenSerializer
from config.permissions import IsOrgMember


@extend_schema(exclude=True)
class AuthTokenCreateView(LoginView):
    def create_token(self):
        token_prefix = self.get_token_prefix()
        expiry = self.get_token_ttl()
        expiry_days = self.request.data.get('expiry_days', None)
        if expiry_days is not None:
            expiry = timedelta(days=int(expiry_days))
        return get_token_model().objects.create(
            name=self.request.data.get('name', None),
            organization=self.request.organization,
            user=self.request.user,
            expiry=expiry,
            prefix=token_prefix
        )


@extend_schema(exclude=True)
class AuthTokenViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, IsOrgMember)

    queryset = AuthToken.objects.order_by('-created')
    serializer_class = AuthTokenSerializer

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """
        Revoke a single token (by digest).
        """
        try:
            token = self.get_object()
            token.delete()
            return Response({"detail": "Token revoked."}, status=status.HTTP_204_NO_CONTENT)
        except AuthToken.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def revoke_all(self, request):
        """
        Revoke all tokens (by org).
        """
        organization = request.organization
        n_deleted, _ = AuthToken.objects.filter(organization=organization).delete()
        return Response({"detail": f"{n_deleted} token(s) revoked."}, status=status.HTTP_200_OK)

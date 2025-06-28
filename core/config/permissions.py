from rest_framework import permissions

from accounts.models import OrganizationMembership


class IsOrgMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'organization'):
            return obj.organization == request.organization
        return False

    def has_permission(self, request, view):
        # Ensure request has organization and user is a member of it
        if not hasattr(request, 'organization'):
            return False
        return OrganizationMembership.objects.filter(
            user=request.user,
            organization=request.organization
        ).exists()


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

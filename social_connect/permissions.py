from rest_framework.permissions import BasePermission


class IsSuperAdminUser(BasePermission):
    """Allows access only to SuperAdmin users."""

    def has_permission(self, request, view):
        """Check condition for the permission."""
        return bool(request.user and request.user.is_superuser)

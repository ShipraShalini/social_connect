from rest_framework.permissions import BasePermission


class IsAuthorised(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.access_req)

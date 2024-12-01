from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow admin users full access and others read-only access.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # SAFE_METHODS contains GET, HEAD, and OPTIONS
            return True
        return request.user and request.user.is_staff

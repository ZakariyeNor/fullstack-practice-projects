from rest_framework import permissions


# Custom permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - Safe methods (GET, HEAD, OPTIONS): everyone can read
    - Unsafe methods (POST, PUT, PATCH, DELETE): only owner or admin can modify
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # If object is a user
        if hasattr(obj, 'pk') and isinstance(obj, type(request.user)):
            return obj == request.user or request.user.is_staff

        # If object has a user field (e.g., Profile)
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff

        return False
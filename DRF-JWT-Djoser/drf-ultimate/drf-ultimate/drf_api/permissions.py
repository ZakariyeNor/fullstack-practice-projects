from rest_framework import permissions

# Custom permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - Safe methods (GET, HEAD, OPTIONS): everyone can read
    - Unsafe methods (POST, PUT, PATCH, DELETE): only owner or admin can modify
    """
    # SAFE
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # UNSAFE
        return obj.owner == request.user
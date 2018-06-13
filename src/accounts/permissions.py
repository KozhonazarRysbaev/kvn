from rest_framework.permissions import BasePermission


class IsAdminOrSelf(BasePermission):
    message = 'Not permission'

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff or request.user.is_superuser or request.user.is_superuser
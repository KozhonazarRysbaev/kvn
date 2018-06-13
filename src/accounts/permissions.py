from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    message = 'Not permission'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
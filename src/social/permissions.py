from rest_framework.permissions import BasePermission


class IsOwnerSelf(BasePermission):
    message = 'Not permission'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

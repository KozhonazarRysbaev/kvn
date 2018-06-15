from rest_framework.permissions import BasePermission


class IsoOwnerSelf(BasePermission):
    message = 'Not permission'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

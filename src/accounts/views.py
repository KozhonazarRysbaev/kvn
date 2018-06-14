from django.http import JsonResponse, Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserSerializer, UserUpdateSerializer
from accounts.models import User
from accounts.permissions import IsSelf


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'patch')

    def get_permissions(self):
        if self.action in ('create', 'list'):
            self.permission_classes = ()
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            self.serializer_class = UserUpdateSerializer
        return super(UserViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        raise Http404


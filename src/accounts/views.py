from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.serializers import UserSerializer, UserUpdateSerializer, PostUserSerializer
from accounts.models import User
from accounts.permissions import IsSelf
from social.models import Post


class UserViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Return a user instance

        list:
            Return all users, ordered by most recently joined.

        create:
            Create a new user.

        partial_update:
            Update one or more fields on an existing user, only owner is available.

        update:
           Update user, only owner is available
        """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'patch')

    def get_permissions(self):
        if self.action in ('create', 'list', 'retrieve'):
            self.permission_classes = ()
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            self.serializer_class = UserUpdateSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        raise Http404


class UserPostViewSet(viewsets.ModelViewSet):
    """
       retrieve:
           Not work, return 404 Not Found

       list:
           Return all posts by user
    """
    serializer_class = PostUserSerializer
    permission_classes = [AllowAny]
    http_method_names = ('get', 'head', 'options')

    def retrieve(self, request, *args, **kwargs):
        raise Http404

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs['user_pk'])

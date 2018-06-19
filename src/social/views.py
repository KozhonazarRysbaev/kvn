from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from social.filters import PostFilter
from social.models import Post
from social.permissions import IsOwnerSelf
from social.serializers import PostSerializer, BasePostSerializer


class PostVieSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a post instance.

    list:
        Return all posts

    create:
        Creates a new post, only for authorized users.

    delete:
        Removes the post, only the owner can remove the post.

    partial_update:
        Update one or more fields on an existing post, only the owner can update the post.

    update:
        Update a post, only the owner can update the post.
    """
    queryset = Post.objects.all()
    serializer_class = BasePostSerializer
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'patch', 'delete')
    filter_class = PostFilter

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsOwnerSelf]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            self.serializer_class = PostSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        post = Post.objects.get(id=instance.id)
        post.views += 1
        post.save()
        return super().retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        post = Post.objects.get(id=instance.id)
        post.is_delete = True
        post.publish = False
        post.save()

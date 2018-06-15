from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from social.models import Post
from social.permissions import IsoOwnerSelf
from social.serializers import PostSerializer


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
    serializer_class = PostSerializer
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'patch', 'delete')

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsoOwnerSelf]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        post = Post.objects.get(id=instance.id)
        post.is_delete = True
        post.publish = False
        post.save()

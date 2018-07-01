from django.db.models import F
from django.db.models.expressions import RawSQL
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from social.filters import PostFilter, TeamFilter
from social.models import Post, Events, Team
from social.permissions import IsOwnerSelf
from social.serializers import PostSerializer, BasePostSerializer, EventSerializer, BaseEventSerializer, \
    BaseTeamSerializer, RatingPost


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

    rating:
        Return all posts, ordered by ratting, filter get parameter /social/posts/rating?content=image, video_file.
    """
    queryset = Post.objects.all().order_by('-created_at')
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

    @action(detail=False)
    def rating(self, request):
        content = request.GET.get('content', 'image')
        crown_query = """
                    SELECT type FROM social_crown WHERE post_id=social_post.id
                """
        post = Post.objects.exclude(**{content: ''}).select_related('user').annotate(
            crown=RawSQL(crown_query, ())).order_by(F('crown').desc(nulls_last=True), F('views').desc(nulls_last=True))

        page = self.paginate_queryset(post)
        if page is not None:
            serializer = RatingPost(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            self.serializer_class = PostSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.publish = False
        instance.save()


class EventVieSet(viewsets.ModelViewSet):
    """
    list:
        Return all event.
    retrieve:
        Return a event instance.
    """
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (AllowAny,)
    queryset = Events.objects.all().order_by('-created_at')
    serializer_class = BaseEventSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            self.serializer_class = EventSerializer
        return super().get_serializer_class()


class TeamVieSet(viewsets.ModelViewSet):
    """
    list:
        Return all teams.
    retrieve:
        Return a team instance.
    """
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (AllowAny,)
    queryset = Team.objects.all()
    serializer_class = BaseTeamSerializer
    filter_class = TeamFilter

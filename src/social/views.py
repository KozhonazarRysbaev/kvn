from datetime import timedelta, date

from django.db.models import F
from django.db.models.expressions import RawSQL
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from social.filters import PostFilter, TeamFilter
from social.models import Post, Events, Team
from social.permissions import IsOwnerSelf
from social.serializers import PostSerializer, BasePostSerializer, EventSerializer, TeamSerializer, BaseEventSerializer, \
    BaseTeamSerializer


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

    def get_queryset(self):
        today = date.today()
        get_sunday = (today - timedelta(days=today.weekday())) - timedelta(days=1)
        get_monday = get_sunday - timedelta(days=7)
        crown_query = """
            SELECT type FROM social_crown WHERE post_id=social_post.id
        """
        return Post.objects.select_related('user').annotate(crown=RawSQL(crown_query, ())).order_by('crown', '-created_at')

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

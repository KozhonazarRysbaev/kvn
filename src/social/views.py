from datetime import timedelta, date

from django.db.models import F
from django.db.models.expressions import RawSQL
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from social.filters import PostFilter, TeamFilter
from social.models import Post, Events, Team, PostComment, PostLike, RequestDonations, Voting
from social.permissions import IsOwnerSelf, IsCommentStatus, IsOwnerTeam, IsVoted, IsVotedUser
from social.serializers import PostSerializer, BasePostSerializer, EventSerializer, BaseEventSerializer, \
    BaseTeamSerializer, RatingPost, PostCommentSerializer, RequestDonationsSerializer, BaseRequestDonationsSerializer, \
    VotingSerializer
from billing.models import CrystalTransaction


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
         crown 0 - gold, 1-silver, 2-bronze
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
        today = date.today()
        get_sunday = (today - timedelta(days=today.weekday())) - timedelta(days=1)
        crown_query = """
                    SELECT type FROM social_crown WHERE post_id=social_post.id AND created_at > '{0}'
                """.format(get_sunday.strftime('%Y-%m-%d %H:%M:%S'))
        crystal_query = """
            SELECT SUM(trans.amount) from billing_crystaltransaction as trans inner join django_content_type as content on content.id=trans.content_type_id where trans.object_id=social_post.id and content.model='post' AND created_at > '{0}'
        """.format(get_sunday.strftime('%Y-%m-%d %H:%M:%S'))
        post = Post.objects.exclude(**{content: ''}).select_related('user').annotate(
            crown=RawSQL(crown_query, ()), crystals=RawSQL(crystal_query, ())).order_by(F('crown').asc(nulls_last=True),
                                                                                        F('views').desc(
                                                                                            nulls_last=True))

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


class PostCommentVieSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a comment instance.

    list:
        Return all comments

    create:
        Creates a new comment, only for authorized users.

    delete:
        Removes the comment, only the owner can remove the comment.

    partial_update:
        Update one or more fields on an existing comment, only the owner can update the comment.

    update:
        Update a comment, only the owner can update the comment.
    """
    permission_classes = [IsAuthenticated, IsCommentStatus]
    serializer_class = PostCommentSerializer
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'patch', 'delete')

    def get_queryset(self):
        return PostComment.objects.filter(post__id=self.kwargs['post_pk'])

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsOwnerSelf, IsCommentStatus]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsCommentStatus]
        else:
            self.permission_classes = [AllowAny, IsCommentStatus]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs['post_pk'])


class LikePostView(RetrieveAPIView):
    """
    get:
        Will return a message, send post_pk.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        like = PostLike.objects.filter(post_id=self.kwargs['post_pk'], user=self.request.user).select_related('user',
                                                                                                              'post')
        if like:
            like.first().delete()
            success = True
            message = "Лайк успешно удален!"
        else:
            post = get_object_or_404(Post, id=self.kwargs['post_pk'])
            like = PostLike(post=post, user=self.request.user)
            like.save()
            success = True
            message = "Лайк успешно добавлен"
        return Response({
            "success": success,
            "message": message
        })


class RequestDonationsVieSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a request donations instance.

    list:
        Return all request donations

    create:
        Creates a new request donations, only for authorized users, Only the captain can apply.
    """
    serializer_class = BaseRequestDonationsSerializer
    queryset = RequestDonations.objects.all().order_by('-created_at')
    http_method_names = ('get', 'head', 'options', 'post')

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsOwnerTeam]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = RequestDonationsSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(team=self.request.user.team_owners.first())


class VotingVieSet(viewsets.ModelViewSet):
    serializer_class = VotingSerializer
    permission_classes = [IsAuthenticated, IsVoted, IsVotedUser]
    http_method_names = ('get', 'head', 'options', 'post')

    def get_queryset(self):
        return Voting.objects.filter(events__pk=self.kwargs['event_pk'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, events_id=self.kwargs['event_pk'])

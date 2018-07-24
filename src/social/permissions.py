from datetime import datetime

from rest_framework.permissions import BasePermission
from django.utils.translation import ugettext_lazy as _
from social.models import Post, Team, RequestDonations, Voting, Events


class IsOwnerSelf(BasePermission):
    message = 'Not permission'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCommentStatus(BasePermission):
    message = _('Пользователь отключил комментарий к этому посту')

    def has_permission(self, request, view):
        if 'post_pk' not in view.kwargs:
            return False
        try:
            return Post.objects.get(pk=view.kwargs['post_pk'], comment_status=True)
        except Post.DoesNotExist:
            return False


class IsOwnerTeam(BasePermission):
    message = 'Not permission'

    def has_permission(self, request, view):
        request_donations = RequestDonations.objects.filter(team=request.user.team_owners.first(),
                                                            is_active=True).first()
        return Team.objects.filter(owner=request.user).exists() if not request_donations else False


class IsVotedUser(BasePermission):
    message = _('Вы уже голосовали!')

    def has_permission(self, request, view):
        if 'event_pk' not in view.kwargs:
            return False

        try:
            v = Voting.objects.get(events__pk=view.kwargs['event_pk'], user=request.user)
            if v:
                return False
        except Voting.DoesNotExist:
            return True


class IsVoted(BasePermission):
    message = _('Устекло время время голосовать!')

    def has_permission(self, request, view):
        if 'event_pk' not in view.kwargs:
            return False

        try:
            return Events.objects.get(pk=view.kwargs['event_pk'], created_at__gt=datetime.now())
        except Events.DoesNotExist:
            return False

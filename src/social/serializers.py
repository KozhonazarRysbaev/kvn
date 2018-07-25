from datetime import datetime

from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User
from location.serializers import CitySerializer
from social.models import Post, Events, Team, PostComment, RequestDonations, Voting


class DateTimeFieldWihTZ(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class UserPostSerializer(serializers.ModelSerializer):
    avatar = HyperlinkedSorlImageField('1024', required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')


class BasePostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(many=False)
    image = HyperlinkedSorlImageField('1024', required=False)
    like_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views', 'like_count',
            'is_like', 'comment_status', 'user')

    def get_like_count(self, obj):
        return obj.post_likes.all().count()

    def get_is_like(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            if obj.post_likes.filter(user=user).exists():
                return True
            else:
                return False
        return False


class RatingPost(BasePostSerializer):
    user = UserPostSerializer(many=False)
    image = HyperlinkedSorlImageField('1024', required=False)
    crown = serializers.IntegerField()
    crystals = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views', 'user',
            'crown', 'crystals')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'comment_status')


class BaseTeamSerializer(serializers.ModelSerializer):
    owner = UserPostSerializer(many=False)
    members = UserPostSerializer(many=True)
    city = CitySerializer(many=False)

    class Meta:
        model = Team
        fields = ('id', 'title', 'logo', 'city', 'owner', 'members')


class TeamSerializer(serializers.ModelSerializer):
    voting_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'title', 'logo', 'voting_count')

    def get_voting_count(self, obj):
        return obj.team_voting.all().count()


class BaseEventSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    created_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")
    expired_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")
    is_voted = serializers.SerializerMethodField()
    is_voting_finish = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ('id', 'title', 'created_at', 'expired_at', 'is_voted', 'is_voting_finish', 'team')

    def get_is_voted(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            try:
                user = Voting.objects.get(events__id=obj.id, user=user)
                if user:
                    return True
            except Voting.DoesNotExist:
                return False
        else:
            return False

    def get_is_voting_finish(self, obj):
        try:
            event = Events.objects.get(pk=obj.id, created_at__gt=datetime.now())
            if event:
                return False
        except Events.DoesNotExist:
            return True


class EventSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    created_at = DateTimeFieldWihTZ(format="%H:%M")
    expired_at = DateTimeFieldWihTZ(format="%H:%M")
    is_voted = serializers.SerializerMethodField()
    is_voting_finish = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ('id', 'title', 'created_at', 'expired_at', 'is_voted', 'is_voting_finish', 'team')

    def get_is_voted(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            try:
                user = Voting.objects.get(events__id=obj.id, user=user)
                if user:
                    return True
            except Voting.DoesNotExist:
                return False
        else:
            return False

    def get_is_voting_finish(self, obj):
        try:
            event = Events.objects.get(pk=obj.id, created_at__gt=datetime.now())
            if event:
                return False
        except Events.DoesNotExist:
            return True


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(many=False, read_only=True)
    created_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'comment', 'created_at', 'user')

    def create(self, validated_data):
        return PostComment.objects.create(**validated_data)


class TeamRequestDonationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'title', 'logo', 'owner')


class BaseRequestDonationsSerializer(serializers.ModelSerializer):
    team = TeamRequestDonationsSerializer(many=False)
    created_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")
    expired_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")

    class Meta:
        model = RequestDonations
        fields = ('id', 'created_at', 'expired_at', 'description', 'team')


class RequestDonationsSerializer(serializers.ModelSerializer):
    expired_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")

    class Meta:
        model = RequestDonations
        fields = ('id', 'expired_at', 'description')


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ('id', 'team')

    def create(self, validated_data):
        try:
            return Voting.objects.create(**validated_data)
        except IntegrityError:
            raise ValidationError('Error! You have already voted')

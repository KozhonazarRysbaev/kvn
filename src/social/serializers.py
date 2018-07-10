from django.utils import timezone
from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User
from location.serializers import CitySerializer
from social.models import Post, Events, Team, PostComment


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

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views', 'user',
            'crown')


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
    class Meta:
        model = Team
        fields = ('id', 'title')


class BaseEventSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    created_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")
    expired_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Events
        fields = ('id', 'title', 'created_at', 'expired_at', 'team')

    def get_status(self, obj):
        return 'true'


class EventSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    created_at = DateTimeFieldWihTZ(format="%H:%M")
    expired_at = DateTimeFieldWihTZ(format="%H:%M")

    class Meta:
        model = Events
        fields = ('id', 'title', 'created_at', 'expired_at', 'team')


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(many=False, read_only=True)
    created_at = DateTimeFieldWihTZ(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'comment', 'created_at', 'user')

    def create(self, validated_data):
        return PostComment.objects.create(**validated_data)

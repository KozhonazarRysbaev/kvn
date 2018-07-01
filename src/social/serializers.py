from django.utils import timezone
from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User
from location.serializers import CitySerializer
from social.models import Post, Events, Team


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

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views', 'user')


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
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height')


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

    # status = serializers.SerializerMethodField()

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

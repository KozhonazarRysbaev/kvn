from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User
from social.models import Post, Events, Team


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
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views', 'user')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'title')


class EventSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ('id', 'title', 'status', 'team')

    def get_status(self, obj):
        return 'true'

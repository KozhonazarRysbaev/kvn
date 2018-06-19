from rest_framework import serializers

from accounts.models import User
from social.models import Post


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class BasePostSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views', 'user')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height')

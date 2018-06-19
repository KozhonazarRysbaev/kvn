from rest_framework import serializers

from social.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height')

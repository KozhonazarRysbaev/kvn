from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User
from social.models import Post


class PostUserSerializer(serializers.ModelSerializer):
    image = HyperlinkedSorlImageField('1024', required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views')


class UserSerializer(serializers.ModelSerializer):
    avatar = HyperlinkedSorlImageField('1024', required=False)
    wallpaper = HyperlinkedSorlImageField('1024', required=False)
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper',
            'post_count')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret.pop('password')
        return ret

    @staticmethod
    def get_post_count(obj):
        return obj.posts.all().count()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'sex', 'avatar', 'date_birth', 'wallpaper', 'first_name', 'last_name')

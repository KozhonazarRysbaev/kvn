from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User
from social.models import Post, RequestTeam


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

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret.pop('password')
        return ret

    @staticmethod
    def get_post_count(obj):
        return obj.posts.all().count()


class UserCreateSerializer(serializers.ModelSerializer):
    avatar = HyperlinkedSorlImageField('1024', required=False)
    wallpaper = HyperlinkedSorlImageField('1024', required=False)
    team_id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper',
            'team_id')

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    phone=validated_data.get('phone', None),
                    sex=validated_data.get('sex', None),
                    avatar=validated_data.get('avatar', None),
                    date_birth=validated_data.get('date_birth', None),
                    first_name=validated_data.get('first_name', None),
                    last_name=validated_data.get('last_name', None),
                    wallpaper=validated_data.get('wallpaper', None),
                    )
        user.set_password(validated_data['password'])
        user.save()
        team_id = validated_data.get('team_id', None)
        if team_id:
            RequestTeam.objects.create(team_id=team_id, user=user)
        return user

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret.pop('password')
        return ret


class RatingUser(UserSerializer):
    views_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper',
            'post_count', 'views_count')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'sex', 'avatar', 'date_birth', 'wallpaper', 'first_name', 'last_name')


class ChangePasswordSerializer(serializers.Serializer):
    """
        Serializer for password change endpoint.
        """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

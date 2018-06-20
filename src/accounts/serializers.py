from rest_framework import serializers, pagination
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
    posts = serializers.SerializerMethodField('paginated_posts')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper',
            'posts')

    def paginated_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        paginator = pagination.LimitOffsetPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostUserSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret.pop('password')
        return ret


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'sex', 'avatar', 'date_birth', 'wallpaper', 'first_name', 'last_name')

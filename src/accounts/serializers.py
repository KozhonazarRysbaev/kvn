from datetime import timedelta, date

from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User, Profession
from social.models import Post, RequestTeam, Team, Crown


class PostUserSerializer(serializers.ModelSerializer):
    image = HyperlinkedSorlImageField('1024', required=False)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'description', 'video_file', 'image', 'image_width', 'image_height', 'views',
            'comment_status')


class UserTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'title', 'logo', 'room')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'name', 'icon')


class UserSerializer(serializers.ModelSerializer):
    avatar = HyperlinkedSorlImageField('1024', required=False)
    wallpaper = HyperlinkedSorlImageField('1024', required=False)
    post_count = serializers.SerializerMethodField()
    team_owners = UserTeamSerializer(many=True)
    team_members = UserTeamSerializer(many=True)
    crystals = serializers.SerializerMethodField()
    profession = ProfessionSerializer()
    pix = serializers.SerializerMethodField()
    gag = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper',
            'post_count', 'team_owners', 'team_members', 'profession', 'crystals', 'pix', 'gag')

    def get_pix(self, obj):
        today = date.today()
        get_sunday = (today - timedelta(days=today.weekday())) - timedelta(days=1)
        crowns = Crown.objects.filter(post__user=obj, created_at__gte=get_sunday, post_type='image').order_by('type')
        if crowns:
            return crowns[0].type
        return None

    def get_gag(self, obj):
        today = date.today()
        get_sunday = (today - timedelta(days=today.weekday())) - timedelta(days=1)
        crowns = Crown.objects.filter(post__user=obj, created_at__gte=get_sunday, post_type='image').order_by('type')
        if crowns:
            return crowns[0].type
        return None

    def get_crystals(self, obj):
        return obj.get_balance()

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret.pop('password')
        return ret

    @staticmethod
    def get_post_count(obj):
        return obj.posts.all().count()


class ProfessionUserSerializer(serializers.ModelSerializer):
    avatar = HyperlinkedSorlImageField('1024', required=False)
    wallpaper = HyperlinkedSorlImageField('1024', required=False)
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper',
            'post_count')

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
            'team_id', 'profession')

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    phone=validated_data.get('phone', None),
                    sex=validated_data.get('sex', None),
                    avatar=validated_data.get('avatar', None),
                    date_birth=validated_data.get('date_birth', None),
                    first_name=validated_data.get('first_name', None),
                    last_name=validated_data.get('last_name', None),
                    wallpaper=validated_data.get('wallpaper', None),
                    profession=validated_data.get('profession', None),
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


class UserCrystalSerializer(serializers.ModelSerializer):
    crystals = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper', 'crystals')

    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        else:
            return None

    def get_crystals(self, obj):
        return obj.get_balance()

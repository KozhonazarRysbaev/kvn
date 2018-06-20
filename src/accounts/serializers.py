from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = HyperlinkedSorlImageField('1024')
    wallpaper = HyperlinkedSorlImageField('1024')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'sex', 'avatar', 'date_birth', 'first_name', 'last_name', 'wallpaper')

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

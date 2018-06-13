from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractUser, \
    PermissionsMixin

from main.utils import avatar_image_path


SEX = (
    ('male', 'Мужской'),
    ('female', 'Женский')
)


class User(AbstractUser):
    """
    Model for storing user, username can be email or facebook id
    """
    phone = models.CharField(max_length=200, verbose_name='Телефон', blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', blank=True, null=True)
    sex = models.CharField(choices=SEX, max_length=30, verbose_name='Пол', null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_image_path, verbose_name=u"Изображение")
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождение')
    email = models.EmailField(verbose_name='email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

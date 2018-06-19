from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, \
    PermissionsMixin

from main.utils import avatar_image_path, wallpaper_image_path


class CustomUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        user = self.model(
            email=kwargs['email']
        )
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.model(
            email=kwargs['email']
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user


SEX = (
    ('male', 'Мужской'),
    ('female', 'Женский')
)


class User(AbstractUser):
    """
    Model for storing user, username can be email or facebook id
    """
    phone = models.CharField(max_length=200, verbose_name='Телефон', blank=True, null=True)
    sex = models.CharField(choices=SEX, max_length=30, verbose_name='Пол', null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_image_path, verbose_name=u"Изображение", null=True, blank=True)
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождение')
    email = models.EmailField(verbose_name='email address', unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    wallpaper = models.ImageField(upload_to=wallpaper_image_path, verbose_name=u"Обои", null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractUser, \
    PermissionsMixin

from main.utils import avatar_image_path, wallpaper_image_path, profession_icon_path


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
    profession = models.ForeignKey('Profession', verbose_name=_('Профессия'), null=True, blank=True,
                                   on_delete=models.SET_NULL)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def default_avatar(self):
        if self.avatar:
            return "{}{}".format(settings.MEDIA_URL, self.avatar)
        return '/media/avatars/494743aa-12f1-4ad6-a6c8-ae70bdd103d2.jpg'


class Profession(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Название'))
    icon = models.ImageField(upload_to=profession_icon_path, verbose_name=_('Иконка'))

    class Meta:
        verbose_name = _('Профессия')
        verbose_name_plural = _('Профессии')

    def __str__(self):
        return self.name

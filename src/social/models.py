from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import City
from main.utils import post_video_path, post_image_path

User = get_user_model()


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('user').filter(is_delete=False, publish=True)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'), blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    video_file = models.FileField(upload_to=post_video_path, verbose_name=_('Видео'), blank=True, null=True,
                                  default=None)
    image = models.ImageField(upload_to=post_image_path, verbose_name=_('Изображение'), blank=True, null=True,
                              height_field='image_height', width_field='image_width', default=None)
    views = models.PositiveIntegerField(default=0, blank=True, verbose_name=u"Просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    edited_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Когда редактирован'))
    publish = models.BooleanField(default=True, verbose_name=_('Опубликован'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Удалена'))

    # store width & height to get them without PIL
    image_width = models.PositiveIntegerField(default=0)
    image_height = models.PositiveIntegerField(default=0)

    all_objects = models.Manager()
    objects = PostManager()

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ['-created_at']


class Team(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('Название'))
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, related_name='team_owners', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='team_members')

    class Meta:
        verbose_name = _('Команда')
        verbose_name_plural = _('Команды')

    def __str__(self):
        return self.title


class RequestTeam(models.Model):
    team = models.ForeignKey(Team, related_name='team_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_requests', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Заявка пользователя')
        verbose_name_plural = _('Заявки пользователя')


class Events(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('Название'))
    created_at = models.DateTimeField(verbose_name=_('Дата и время начала'))
    expired_at = models.DateTimeField(verbose_name=_('Дата и время истечение'))
    team = models.ManyToManyField(Team, related_name='event_teams')

    class Meta:
        verbose_name = _('Событие')
        verbose_name_plural = _('События')

    def __str__(self):
        return self.title

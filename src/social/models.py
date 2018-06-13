from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from main.utils import post_video_path, post_image_path

User = get_user_model()


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user').filter(is_delete=False, publish=True)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'), blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    video_file = models.FileField(upload_to=post_video_path, verbose_name=_('Видео'), blank=True, null=True)
    image = models.ImageField(upload_to=post_image_path, verbose_name=_('Изображение'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    edited_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Когда редактирован'))
    publish = models.BooleanField(default=True, verbose_name=_('Опубликован'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Удалена'))

    all_objects = models.Manager()
    objects = PostManager()

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')

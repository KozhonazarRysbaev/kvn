from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import City
from main.utils import post_video_path, post_image_path, team_logo_path
from billing.models import CrystalTransaction

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
    comment_status = models.BooleanField(default=True, verbose_name=_('Разрешение на комментарий'))

    all_objects = models.Manager()
    objects = PostManager()

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ['-created_at']


class PostComment(models.Model):
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name=_('Комментарий'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    edited_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Когда редактирован'))

    class Meta:
        verbose_name = _('Комментарий поста')
        verbose_name_plural = _('Комментарии постов')
        ordering = ['-created_at']


class Team(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('Название'))
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, related_name='team_owners', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='team_members')
    logo = models.ImageField(upload_to=team_logo_path, verbose_name=_('Лого'))

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


post_type = (
    ('image', 'Фотографии'),
    ('video_file', 'Видео')
)


class Crown(models.Model):
    post = models.ForeignKey(Post, related_name='crowns', on_delete=models.CASCADE, unique=True)
    type = models.IntegerField(verbose_name=_('Тип короны'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    post_type = models.CharField(choices=post_type, max_length=50)

    class Meta:
        verbose_name = _('Корона')
        verbose_name_plural = _('Короны')

    @classmethod
    def create_result_last_week(cls):
        today = date.today()
        get_sunday = (today - timedelta(days=today.weekday())) - timedelta(days=1)
        get_monday = get_sunday - timedelta(days=7)
        crown = slice(0, 3)
        crystal = slice(0, 15)
        image_query = Post.objects.filter(created_at__range=(get_monday, get_sunday + timedelta(days=1)),
                                          crowns__isnull=True).exclude(image='').order_by(
            '-views')
        video_query = Post.objects.filter(created_at__range=(get_monday, get_sunday + timedelta(days=1)),
                                          crowns__isnull=True).exclude(video_file='').order_by(
            '-views')
        CrystalTransaction.objects.bulk_create(
            [CrystalTransaction(user=post[1].user, amount=1, content_object=post[1], action='cash_in') for post in
             enumerate(image_query[crystal])]
        )
        CrystalTransaction.objects.bulk_create(
            [CrystalTransaction(user=post[1].user, amount=1, content_object=post[1], action='cash_in') for post in
             enumerate(video_query[crystal])]
        )
        Crown.objects.bulk_create(
            [Crown(post=post[1], type=post[0], post_type='image') for post in enumerate(image_query[crown])])
        Crown.objects.bulk_create(
            [Crown(post=post[1], type=post[0], post_type='video_file') for post in enumerate(video_query[crown])])


class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Лайк')
        verbose_name_plural = _('Лайки')


class RequestDonationsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class RequestDonations(models.Model):
    team = models.ForeignKey(Team, related_name='team_request_donations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    expired_at = models.DateTimeField(verbose_name=_('Дата и время истечение'))
    description = models.TextField(verbose_name=_('Описание'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активен'))

    all_objects = models.Manager()
    objects = RequestDonationsManager()

    class Meta:
        verbose_name = _('Запрос на пожертвования')
        verbose_name_plural = _('Запросы на пожертвования')

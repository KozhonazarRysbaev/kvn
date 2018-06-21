# Generated by Django 2.0.6 on 2018-06-21 17:00

from django.db import migrations, models
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20180621_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, height_field='image_height', null=True, upload_to=main.utils.post_image_path, verbose_name='Изображение', width_field='image_width'),
        ),
        migrations.AlterField(
            model_name='post',
            name='video_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to=main.utils.post_video_path, verbose_name='Видео'),
        ),
    ]

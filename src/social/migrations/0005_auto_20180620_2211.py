# Generated by Django 2.0.6 on 2018-06-20 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_post_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]

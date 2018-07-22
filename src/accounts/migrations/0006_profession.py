# Generated by Django 2.0.6 on 2018-07-11 21:43

from django.db import migrations, models
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_wallpaper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('icon', models.ImageField(upload_to=main.utils.profession_icon_path, verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Профессия',
                'verbose_name_plural': 'Профессии',
            },
        ),
    ]
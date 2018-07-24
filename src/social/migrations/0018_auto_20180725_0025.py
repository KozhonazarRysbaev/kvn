# Generated by Django 2.0.6 on 2018-07-24 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0017_requestdonations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_voting', to='social.Events')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_voting', to='social.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_voting', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Голос',
                'verbose_name_plural': 'Голоса',
            },
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together={('events', 'team', 'user')},
        ),
    ]
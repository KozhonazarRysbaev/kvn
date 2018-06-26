from django.contrib import admin

from social.models import Post, Team, Events, RequestTeam

admin.site.register(Post)
admin.site.register(Team)
admin.site.register(Events)
admin.site.register(RequestTeam)

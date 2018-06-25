from django.contrib import admin

from location.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(City, CityAdmin)

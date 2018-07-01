from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
import django_filters

from location.models import City
from social.models import Post, Team


class PostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label=_('Поиск'), method='search_post')

    class Meta:
        model = Post
        fields = ('title', 'description')

    def search_post(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))


class TeamFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ('title',)


class CityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = City
        fields = ('name',)

import django_filters
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from accounts.models import User


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label=_('Поиск'), method='search_user')

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def search_user(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))

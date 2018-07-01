from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from location.models import City
from location.serializers import CitySerializer
from social.filters import CityFilter


class CityViewSet(ModelViewSet):
    """
    list:
        Return all cities.
    retrieve:
        Return a city instance.
    """
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_class = CityFilter

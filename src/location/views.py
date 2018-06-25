from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from location.models import City
from location.serializers import CitySerializer


class CityViewSet(ModelViewSet):
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer
    queryset = City.objects.all()

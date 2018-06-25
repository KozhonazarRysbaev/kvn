from django.urls import include, path
from rest_framework.routers import SimpleRouter

from location.views import CityViewSet

router = SimpleRouter()
router.register(r'city', CityViewSet, 'city')

app_name = 'location'
urlpatterns = [
    path('', include(router.urls))
]

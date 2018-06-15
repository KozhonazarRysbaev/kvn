
from django.urls import path, include
from rest_framework import routers

from social import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', views.PostVieSet, base_name='posts')

urlpatterns = [
    path(r'', include(router.urls)),
]

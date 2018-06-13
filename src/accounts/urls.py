
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework import routers

from accounts import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token)
]

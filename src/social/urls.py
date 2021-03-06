from django.urls import path, include
from rest_framework import routers

from social import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', views.PostVieSet, base_name='posts')
router.register(r'posts/(?P<post_pk>[0-9]+)/comments', views.PostCommentVieSet, base_name='post_comments')
router.register(r'events', views.EventVieSet, base_name='events')
router.register(r'events/(?P<event_pk>[0-9]+)/voting', views.VotingVieSet, base_name='event_voting')
router.register(r'teams', views.TeamVieSet, base_name='teams')
router.register(r'donations', views.RequestDonationsVieSet, base_name='donations')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'like/add/<int:post_pk>', views.LikePostView.as_view(), name='add_like'),
]

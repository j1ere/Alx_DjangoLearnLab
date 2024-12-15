from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'posts/(?P<post_pk>[^/.]+)/comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedView.as_view(), name='feed'),

    path('<int:pk>/like/',  views.LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/',  views.UnlikePostView.as_view(), name='unlike-post'),
]
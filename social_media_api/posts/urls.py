from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'posts/(?P<post_pk>[^/.]+)/comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
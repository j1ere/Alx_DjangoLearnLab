from django.urls import path
from . import views

follow_view = views.FollowViewSet.as_view({
    'post': 'follow',
    'post': 'unfollow'
})
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name = "login"),

    path('follow/<int:pk>/', views.FollowViewSet.as_view({'post': 'follow'}), name='follow'),
    path('unfollow/<int:pk>/', views.FollowViewSet.as_view({'post': 'unfollow'}), name='unfollow'),
    path('followers/', views.FollowViewSet.as_view({'get': 'followers'}), name='followers'),
    path('following/', views.FollowViewSet.as_view({'get': 'following'}), name='following'),
]
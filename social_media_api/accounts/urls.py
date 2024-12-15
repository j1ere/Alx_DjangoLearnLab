from django.urls import path
from . import views

follow_view = views.FollowViewSet.as_view({
    'post': 'follow',
    'post': 'unfollow'
})
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name = "login"),

    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
]
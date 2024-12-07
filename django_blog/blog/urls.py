from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('posts/', views.posts_view, name="posts"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('post/', views.posts_view, name="posts"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile_view, name="profile"),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/edit/<int:pk>/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]

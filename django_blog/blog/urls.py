from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('posts/', views.posts_view, name="posts"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile_view, name="profile"),
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('blog/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comments/edit/<int:pk>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comments/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
]

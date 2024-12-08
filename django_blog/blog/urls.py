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
    path('tags/<str:tag_name>/search/', views.posts_by_tag, name='posts_by_tag'),

    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
]

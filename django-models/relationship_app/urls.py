from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, book_list_view  # Import necessary views

urlpatterns = [
    path('books/', views.book_list_view, name='book_list'),  # URL for the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # URL for the class-based view


    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('books/', book_list_view, name='book_list'),  # Example URL for redirection after login
    # Add other views and URLs as needed


]

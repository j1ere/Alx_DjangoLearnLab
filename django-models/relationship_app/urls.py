from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list_view, name='book_list'),  # URL for the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # URL for the class-based view


    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('books/', views.book_list_view, name='book_list'),  # Example URL for redirection
    # Add other views and URLs as needed


]

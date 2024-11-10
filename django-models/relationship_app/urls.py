from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, book_list_view  # Import necessary views
from .views import admin_view, librarian_view, member_view


urlpatterns = [
     path('book/add/', views.add_book, name='add_book'),
    path('book/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    path('books/', views.book_list_view, name='book_list'),  # URL for the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # URL for the class-based view


    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('books/', book_list_view, name='book_list'),  # Example URL for redirection after login
    # Add other views and URLs as needed


]

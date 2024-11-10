from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library, Book  # Import both Book and Library models
from django.views.generic.detail import DetailView
from .views import list_books


from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Custom view for user registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('book_list')  # Redirect to a page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Login view using Django's built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# Logout view using Django's built-in LogoutView
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'














# Function-based view to list all books with their authors
def book_list_view(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display details of a specific library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

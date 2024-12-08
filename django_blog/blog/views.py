from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def home_view(request):
    """
    Renders the home page.
    
    The home page provides an overview of the blog with featured posts.
    """
    return render(request, 'blog/base.html')

@login_required
def posts_view(request):
    """
    Renders the posts page.
    
    Displays a list of all blog posts with pagination support.
    """
    return render(request, 'posts.html')

def login_view(request):
    """
    Handles user authentication for login.

    - Displays the login form.
    - Authenticates users based on username and password.
    - Redirects authenticated users to the home page.
    - If authentication fails, an error message is displayed.

    Arguments:
    request -- HTTP request object.
    """
    if request.method == "POST":
        # Retrieve username and password from POST data
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'blog/login.html')

def register_view(request):
    """
    Handles user registration.

    - Utilizes CustomUserCreationForm to create new users.
    - Upon successful registration, redirects users to the login page.
    - Displays errors if form validation fails.

    Arguments:
    request -- HTTP request object.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            # Errors are displayed if the form is invalid
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.

    - Logs out the currently authenticated user.
    - Redirects to the home page with a success message.

    Arguments:
    request -- HTTP request object.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    """
    Allows authenticated users to view and edit their profile details.

    - Displays the profile form pre-filled with user details.
    - Handles form submission to update user details.
    - Redirects to the profile page with a success message upon update.

    Arguments:
    request -- HTTP request object.
    """
    if request.method == 'POST':
        # Populate form with POST data and the authenticated user instance
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        # Pre-fill the form with current user data
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'auth/profile.html', {'form': form})

# @login_required
# def profile_view(request):
#     if request.method == "POST":
#         user = request.user
#         user.email = request.POST.get('email', user.email)
#         user.first_name = request.POST.get('first_name', user.first_name)
#         user.last_name = request.POST.get('last_name', user.last_name)
#         user.save()
#         messages.success(request, "Profile updated successfully.")
#         return redirect('profile')
#     return render(request, 'auth/profile.html')
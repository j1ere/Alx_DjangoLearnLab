from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, CommentForm
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

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
    return render(request, 'blog/profile.html', {'form': form})


# View to display a list of all blog posts.
class PostListView(ListView):
    """
    A view that lists all the blog posts.
    
    Inherits from ListView. This view retrieves all the posts from the 
    database and renders them in a template. It uses the 'blog/post_list.html' 
    template and passes the list of posts to the template under the context name 'posts'.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  # Context name for the list of posts in the template.

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.all()
    

# View to display a single post with detailed information.
class PostDetailView(DetailView):
    """
    A view to display a detailed view of a single blog post.
    
    Inherits from DetailView. This view retrieves a single blog post based on its primary key 
    and renders it using the 'blog/post_detail.html' template. The post object is passed to the 
    template under the context name 'post'.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # Context name for the post object in the template.

# View to handle the creation of a new blog post.
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    A view for authenticated users to create a new blog post.
    
    Inherits from CreateView and requires the user to be logged in (LoginRequiredMixin).
    The form includes fields for the title and content of the post. Upon successful form submission, 
    the author is automatically set to the logged-in user. The user is redirected to the post list 
    upon successful creation.
    """
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect to the post list view after successful creation.

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Process tags and associate them with the post
        tags = form.cleaned_data['tags']
        if tags:
            tag_names = {tag.strip() for tag in tags.split(',') if tag.strip()}  # Ensure no duplicates
            tags_objects = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            form.instance.tags.set(tags_objects)  # Associate the tags with the post
        return super().form_valid(form)

# View to handle the update/edit of an existing blog post.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view for authenticated users (who are the post authors) to update an existing blog post.
    
    Inherits from UpdateView and requires the user to be logged in (LoginRequiredMixin) and to be the 
    author of the post (UserPassesTestMixin). This view allows users to modify the title and content 
    of the post. Upon successful form submission, the user is redirected to the updated post's detail page.
    """
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        """
        This method dynamically returns the URL for the updated post using its primary key (pk).
        This ensures that the user is redirected to the post's detail page after successfully updating it.
        """
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Process tags and associate them with the post
        tags = form.cleaned_data['tags']
        if tags:
            tag_names = {tag.strip() for tag in tags.split(',') if tag.strip()}  # Ensure no duplicates
            tags_objects = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            form.instance.tags.set(tags_objects)  # Update the post with the new tags
        return super().form_valid(form)

    def test_func(self):
        """
        This method checks whether the current user is the author of the post.
        It returns True if the user is the author, allowing them to edit the post.
        """
        post = self.get_object()
        return self.request.user == post.author

# View to handle the deletion of an existing blog post.
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A view for authenticated users (who are the post authors) to delete a blog post.
    
    Inherits from DeleteView and requires the user to be logged in (LoginRequiredMixin) and to be the 
    author of the post (UserPassesTestMixin). This view allows the author to delete their post. Upon successful 
    deletion, the user is redirected to the homepage.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')  # Redirect to the homepage after successful deletion.

    def test_func(self):
        """
        This method checks whether the current user is the author of the post.
        It returns True if the user is the author, allowing them to delete the post.
        """
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['post_id']
        context['post'] = get_object_or_404(Post, id=post_id)
        return context

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Use reverse to get the URL string and return it
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_id']})
    

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def form_valid(self, form):
        # Ensure that the logged-in user is the author of the comment
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the post's detail page after the comment is updated
        #return redirect('post_detail', pk=self.object.post.pk)
         # Use reverse to get the URL string and return it
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Ensure only the author of the comment can edit it
        comment = self.get_object()
        return self.request.user == comment.author
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        # Ensure only the author of the comment can delete it
        comment = self.get_object()
        return self.request.user == comment.author


def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})




class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Adjust the template to show posts filtered by tag
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)
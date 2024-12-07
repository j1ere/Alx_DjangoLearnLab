from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'blog/base.html')

def posts_view(request):
    pass

def login_view(request):
    ...

def register_view(request):
    pass

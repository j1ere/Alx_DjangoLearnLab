from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework 
#from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
# Retrieve all books

# List all books
# class BookListView(ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

class BookListView(ListAPIView):
    """
    View to list all books with filtering, searching, and ordering capabilities.
    - Filtering: Use query parameters (e.g., `?title=Sample` or `?publication_year=2023`).
    - Searching: Use `?search=<term>` to search title or author name.
    - Ordering: Use `?ordering=title` or `?ordering=-publication_year` to sort results.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering

# Retrieve a specific book by ID
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Create a new book (Authenticated users only)
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Update an existing book (Admin only or custom permissions)
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

# Delete a book (Admin only or custom permissions)
class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
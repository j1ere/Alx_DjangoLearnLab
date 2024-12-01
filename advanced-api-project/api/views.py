from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.filters import SearchFilter
# Create your views here.
# Retrieve all books

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author__name'] 
# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Open for read-only access


# Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to add custom logic during creation.
        For example, attach the current user if required.
        """
        serializer.save()


# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only


# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only

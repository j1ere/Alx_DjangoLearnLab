from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book  # Reference to the Book model
        fields = '__all__'  # Include all fields of the model

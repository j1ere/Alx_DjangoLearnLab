from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    A form for adding or updating books in the library.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter book title', 'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255)
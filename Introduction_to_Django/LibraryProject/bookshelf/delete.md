#deleting all records in Book model

from bookshelf.models import Book
Book.objects.all().delete()
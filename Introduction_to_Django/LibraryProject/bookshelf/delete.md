#deleting all records in Book model

from bookshelf.models import Book

book.delete()
# Confirming deletion by retrieving all books
Book.objects.all()
<QuerySet []>
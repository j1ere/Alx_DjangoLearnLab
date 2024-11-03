#retrieving all records from a database model
from bookshelf.models import Book
retrieve = Book.objects.all()
print(retrieve)
<QuerySet [<Book: Book object (1)>]>

##creating an object instance in the model Book
book_instance = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)

#retrieving all records from a database model
from bookshelf.models import Book
retrieve = Book.objects.all()
print(retrieve)
<QuerySet [<Book: Book object (1)>]>

#updating records in models 
update_record = Book.objects.update(title="Nineteen Eighty-Four")
retrieve_books = Book.objects.all()
retrieve_books
<QuerySet [<Book: Book object (1)>]>

#deleting all records in Book model

from bookshelf.models import Book
Book.objects.all().delete()
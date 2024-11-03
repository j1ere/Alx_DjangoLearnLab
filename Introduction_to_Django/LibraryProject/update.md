#updating records in models 
update_record = Book.objects.update(title="Nineteen Eighty-Four")
retrieve_books = Book.objects.all()
retrieve_books
<QuerySet [<Book: Book object (1)>]>
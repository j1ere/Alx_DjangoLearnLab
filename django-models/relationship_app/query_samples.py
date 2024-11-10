from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author using filter
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return []

# List all books in a library using filter
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()  # No change needed here since it's already fetching related objects
    except Library.DoesNotExist:
        return []

# Retrieve the librarian for a library using filter
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian  # No change needed here as this is a one-to-one relationship
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

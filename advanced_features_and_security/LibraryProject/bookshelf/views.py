from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from myapp.models import Book

@permission_required('myapp.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('myapp.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        # Handle book creation logic
        title = request.POST.get('title')
        author = request.POST.get('author')
        Book.objects.create(title=title, author=author)
        return HttpResponse("Book created successfully")
    return render(request, 'bookshelf/book_form.html')

@permission_required('myapp.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        # Handle book update logic
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.save()
        return HttpResponse("Book updated successfully")
    return render(request, 'bookshelf/book_form.html', {'book': book})

@permission_required('myapp.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return HttpResponse("Book deleted successfully")

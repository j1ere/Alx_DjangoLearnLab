from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book

class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API endpoints.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create some sample books
        self.book1 = Book.objects.create(title="Book One", author="Author One", publication_year=2020)
        self.book2 = Book.objects.create(title="Book Two", author="Author Two", publication_year=2021)
        # URLs
        self.list_url = "/api/books/"
        self.detail_url = lambda pk: f"/api/books/{pk}/"

    def test_list_books(self):
        """
        Test retrieving the list of books.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """
        Test retrieving a single book by ID.
        """
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_authenticated(self):
        """
        Test creating a book as an authenticated user.
        """
        self.client.login(username="testuser", password="password")
        data = {"title": "New Book", "author": "New Author", "publication_year": 2023}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """
        Test creating a book as an unauthenticated user.
        """
        data = {"title": "Unauthorized Book", "author": "Unknown", "publication_year": 2023}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """
        Test updating a book as an authenticated user.
        """
        self.client.login(username="testuser", password="password")
        data = {"title": "Updated Title", "author": "Updated Author", "publication_year": 2021}
        response = self.client.put(self.detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        """
        Test deleting a book as an authenticated user.
        """
        self.client.login(username="testuser", password="password")
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_search_books(self):
        """
        Test searching for books by title or author.
        """
        response = self.client.get(f"{self.list_url}?search=Author One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ordering_books(self):
        """
        Test ordering books by publication year.
        """
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Book One")

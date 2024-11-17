from django.test import TestCase
from .models import Book

class BookSearchTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="Secure Django")

    def test_search_books(self):
        response = self.client.get('/search/?query=Django')
        self.assertContains(response, "Secure Django")

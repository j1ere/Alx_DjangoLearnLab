from django.test import TestCase
from .forms import ExampleForm
from .models import Author

class ExampleFormTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jane Doe")

    def test_valid_form(self):
        form_data = {'title': 'Django for Beginners', 'author': self.author.id}
        form = ExampleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'title': ''}
        form = ExampleForm(data=form_data)
        self.assertFalse(form.is_valid())

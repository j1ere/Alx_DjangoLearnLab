from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=100, null=True)
    publication_year = models.IntegerField(default=0)



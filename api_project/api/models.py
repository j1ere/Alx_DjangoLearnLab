from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=240)
    author = models.CharField(max_length=150)
    publish_date = models.DateField()
    

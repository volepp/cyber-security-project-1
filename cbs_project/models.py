from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.TextField(default="N/A")
    read = models.BooleanField(default=False)
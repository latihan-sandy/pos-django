from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank = True)
    created_at = models.DateField(blank = True)

    def __str__(self):
        return self.name
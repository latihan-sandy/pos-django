from django.db import models
from django.urls import reverse


# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    website = models.CharField(max_length=30)
    address = models.TextField(blank = True)
    created_at = models.DateField(blank = True)

    def __str__(self):
        return self.name
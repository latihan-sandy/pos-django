from django.db import models
from django.urls import reverse
#relations
from brands.models import Brand
from genres.models import Type
from suppliers.models import Supplier
from categories.models import Category


# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    # brand
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL,null=True)
    # type
    genre = models.ForeignKey(Type, on_delete=models.SET_NULL,null=True)
    # supplier
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True)
    # categories
    categories = models.ManyToManyField(Category, related_name='categories')
    #others
    stock = models.PositiveIntegerField(default=0)
    price_purchase = models.FloatField(default=0)
    price_sales = models.FloatField(default=0)
    price_profit = models.FloatField(default=0)
    date_expired = models.DateField(blank = True)
    description = models.TextField(blank = True)
    notes = models.TextField(blank = True)
    image = models.TextField(blank = True)
    created_at = models.DateField(blank = True)
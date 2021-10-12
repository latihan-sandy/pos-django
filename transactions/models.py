from django.db import models
#Relations
from suppliers.models import Supplier
from customers.models import Customer
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    typeof = models.PositiveIntegerField(default=0)
    status = models.PositiveIntegerField(default=0)
    invoice_number = models.CharField(max_length=30)
    invoice_date = models.DateField(blank = True)
    # supplier
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True)
    # customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    # casheir
    casheir = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    # Others
    total_items = models.PositiveIntegerField(default=0)
    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    grandtotal = models.FloatField(default=0)
    cash = models.FloatField(default=0)
    change = models.FloatField(default=0)
    notes = models.TextField(blank = True)
    created_at = models.DateField(blank = True)


class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
# Generated by Django 3.0 on 2019-12-24 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeof', models.PositiveIntegerField(default=0)),
                ('status', models.PositiveIntegerField(default=0)),
                ('invoice_number', models.CharField(max_length=30)),
                ('invoice_date', models.DateField(blank=True)),
                ('total_items', models.PositiveIntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('grandtotal', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('cash', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('change', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateField(blank=True)),
                ('casheir', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.Customer')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='suppliers.Supplier')),
            ],
        ),
    ]
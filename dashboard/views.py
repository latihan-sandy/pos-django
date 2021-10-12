from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.core import serializers
from django.db.models import Q
from django.db.models import Sum
import json as simplejson
import calendar
# Model Import
from products.models import Product
from suppliers.models import Supplier
from brands.models import Brand
from customers.models import Customer
from transactions.models import Transaction
from transactions.models import TransactionDetail

# Create your views here.
@login_required
def index(request):
    return render(request, "app/dashboard/index.html", {'title': 'All Brand Price'})


@login_required
def api(request):
    options = {
        "product": Product.objects.count(),
        "supplier": Supplier.objects.count(),
        "customer": Customer.objects.count(),
        "brand": Brand.objects.count(),
        "purchase": purchase_dashboard(),
        "sale": sale_dashboad(),
        "chartPurchase": report_year(1),
        "chartSale": report_year(1)
    }
    return JsonResponse(options, safe=False)

def purchase_dashboard():

    current_year = str(datetime.now().year)
    current_month = str(datetime.now().month)

    if(datetime.now().month < 10):
        current_month  = "0"+current_month
        
    lastDate = calendar.monthrange(datetime.now().year, datetime.now().month)[1]

    date_first = current_year+"-"+current_month+"-"+"01"
    date_last = current_year+"-"+current_month+"-"+str(lastDate)

    sql = '''
         SELECT 
            products_product.id as id,
            products_product.name as name,
            SUM(qty) as total
        FROM transactions_transactiondetail 
        INNER JOIN products_product ON products_product.id = transactions_transactiondetail.product_id
        INNER JOIN transactions_transaction ON transactions_transaction.id = transactions_transactiondetail.transaction_id
        WHERE transactions_transaction.status = 1
        AND DATE(transactions_transaction.invoice_date) >= '[first_date]' AND DATE(transactions_transaction.invoice_date) <= '[last_date]' AND transactions_transaction.typeof = 0
        GROUP BY products_product.id, products_product.name, qty
        ORDER BY qty DESC 
        LIMIT 10
    '''
    sql = sql.replace("[first_date]", str(date_first))
    sql = sql.replace("[last_date]", str(date_last))
    listData = list(TransactionDetail.objects.raw(sql))

    result = []
    for row in listData:
        result.append({
            "name":row.name,
            "total":float(row.total)
        })
        

    return result

def sale_dashboad():
    current_year = str(datetime.now().year)
    current_month = str(datetime.now().month)

    if(datetime.now().month < 10):
        current_month  = "0"+current_month
        
    lastDate = calendar.monthrange(datetime.now().year, datetime.now().month)[1]

    date_first = current_year+"-"+current_month+"-"+"01"
    date_last = current_year+"-"+current_month+"-"+str(lastDate)

    sql = '''
        SELECT 
            products_product.id as id,
            products_product.name as name,
            SUM(qty) as total
        FROM transactions_transactiondetail 
        INNER JOIN products_product ON products_product.id = transactions_transactiondetail.product_id
        INNER JOIN transactions_transaction ON transactions_transaction.id = transactions_transactiondetail.transaction_id
        WHERE transactions_transaction.status = 1
        AND DATE(transactions_transaction.invoice_date) >= '[first_date]' AND DATE(transactions_transaction.invoice_date) <= '[last_date]' AND transactions_transaction.typeof = 1
        GROUP BY products_product.id, products_product.name, qty
        ORDER BY qty DESC 
        LIMIT 10
    '''
    sql = sql.replace("[first_date]", str(date_first))
    sql = sql.replace("[last_date]", str(date_last))
    listData = list(TransactionDetail.objects.raw(sql))

    result = []
    for row in listData:
        result.append({
            "name":row.name,
            "total":float(row.total)
        })
        

    return result

def report_year(type):

    result = []
    current_year = str(datetime.now().year)
    
    i = 1
    while(i <= 12):
        
        current_month = str(i)

        lastDate = calendar.monthrange(datetime.now().year, i)[1]

        if(i < 10):
            current_month  = "0"+current_month

        date_first = current_year+"-"+current_month+"-"+"01"
        date_last = current_year+"-"+current_month+"-"+str(lastDate)
        transaction = Transaction.objects.filter(typeof = type, status = 1, invoice_date__range = (date_first, date_last)).aggregate(Sum('grandtotal'))["grandtotal__sum"] or 0.00
        result.append(transaction)
        i += 1

    return result

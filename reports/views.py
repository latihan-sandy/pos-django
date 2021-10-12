from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime
from transactions.models import Transaction
from suppliers.models import Supplier
from customers.models import Customer
from products.models import Product
import calendar

# Create your views here.
@login_required
def index(request, template_name='app/reports/index.html'):
    current_year = str(datetime.now().year)
    current_month = str(datetime.now().month)

    if(datetime.now().month < 10):
        current_month  = "0"+current_month
        
    lastDate = calendar.monthrange(datetime.now().year, datetime.now().month)[1]

    date_first = current_year+"-"+current_month+"-"+"01"
    date_last = current_year+"-"+current_month+"-"+str(lastDate)

    return render(request, template_name, { "date_first" : date_first, "date_last" : date_last })


@login_required
def purchase_period(request, date_first, date_last, template_name='app/reports/purchase_period.html'):
    first = datetime.strptime(date_first, "%Y-%m-%d")
    last = datetime.strptime(date_last, "%Y-%m-%d")
    transaction = Transaction.objects.filter(typeof = 0, status = 1, invoice_date__range = (first, last)).order_by("-id").all()
    return render(request, template_name, { "data" : transaction })


@login_required
def purchase_supplier(request, date_first, date_last, template_name='app/reports/purchase_supplier.html'):
    sql = '''
         SELECT 
            suppliers_supplier.id as id,
            suppliers_supplier.id as supplier_id,
            suppliers_supplier.name as supplier_name,
            IFNULL(SUM(qty), 0) as total_buy,
            IFNULL(SUM(total),0) as total_purchase
        FROM 
        suppliers_supplier
        LEFT JOIN transactions_transaction ON transactions_transaction.supplier_id = suppliers_supplier.id
        LEFT JOIN transactions_transactiondetail ON transactions_transaction.id = transactions_transactiondetail.transaction_id
        WHERE transactions_transaction.status = 1
        AND DATE(transactions_transaction.invoice_date) >= '[first_date]' AND DATE(transactions_transaction.invoice_date) <= '[last_date]' AND transactions_transaction.typeof = 0
        GROUP BY suppliers_supplier.id, suppliers_supplier.name ORDER BY suppliers_supplier.name
    '''
    sql = sql.replace("[first_date]",str(date_first))
    sql = sql.replace("[last_date]",str(date_last))
    listData = Supplier.objects.raw(sql)
    return render(request, template_name, { "data" : listData })

@login_required
def purchase_product(request, date_first, date_last, template_name='app/reports/purchase_product.html'):
    sql = '''
    SELECT 
        products_product.id as id,
        brands_brand.name as brand_name,
        genres_type.name as type_name,
        products_product.sku as product_sku,
        products_product.name as product_name,
        suppliers_supplier.name as supplier_name,
        SUM(qty) as total_buy,
        SUM(total) as total_purchase

    FROM products_product
        LEFT JOIN transactions_transactiondetail ON transactions_transactiondetail.product_id = products_product.id
        LEFT JOIN transactions_transaction ON transactions_transaction.id = transactions_transactiondetail.transaction_id
        LEFT JOIN brands_brand ON brands_brand.id = products_product.brand_id
        LEFT JOIN genres_type ON genres_type.id = products_product.genre_id
        LEFT JOIN suppliers_supplier ON suppliers_supplier.id = products_product.supplier_id
        WHERE DATE(transactions_transaction.invoice_date) >= '[first_date]' AND DATE(transactions_transaction.invoice_date) <= '[last_date]' AND transactions_transaction.typeof = 1
        GROUP BY brands_brand.name, genres_type.name, products_product.sku, products_product.name, suppliers_supplier.name ORDER BY brands_brand.name, genres_type.name, suppliers_supplier.name, products_product.sku, products_product.name 
    '''
    sql = sql.replace("[first_date]",str(date_first))
    sql = sql.replace("[last_date]",str(date_last))
    listData = Product.objects.raw(sql)
    return render(request, template_name, { "data" : listData })

@login_required
def sale_period(request, date_first, date_last, template_name='app/reports/sale_period.html'):
    first = datetime.strptime(date_first, "%Y-%m-%d")
    last = datetime.strptime(date_last, "%Y-%m-%d")
    transaction = Transaction.objects.filter(typeof = 1, status = 1, invoice_date__range = (first, last)).order_by("-id").all()
    return render(request, template_name, { "data" : transaction })


@login_required
def sale_customer(request, date_first, date_last, template_name='app/reports/sale_customer.html'):
    sql = '''
         SELECT 
            customers_customer.id as id,
            customers_customer.id as customer_id,
            customers_customer.name as customer_name,
            IFNULL(SUM(qty), 0) as total_buy,
            IFNULL(SUM(total),0) as total_sale
        FROM 
        customers_customer
        LEFT JOIN transactions_transaction ON transactions_transaction.customer_id = customers_customer.id
        LEFT JOIN transactions_transactiondetail ON transactions_transaction.id = transactions_transactiondetail.transaction_id
        WHERE transactions_transaction.status = 1
        AND DATE(transactions_transaction.invoice_date) >= '[first_date]' AND DATE(transactions_transaction.invoice_date) <= '[last_date]' AND transactions_transaction.typeof = 1
        GROUP BY customers_customer.id, customers_customer.name ORDER BY customers_customer.name
    '''
    sql = sql.replace("[first_date]",str(date_first))
    sql = sql.replace("[last_date]",str(date_last))
    listData = Customer.objects.raw(sql)
    return render(request, template_name, { "data" : listData })

@login_required
def sale_product(request, date_first, date_last, template_name='app/reports/sale_product.html'):
    sql = '''
    SELECT 
        products_product.id as id,
        brands_brand.name as brand_name,
        genres_type.name as type_name,
        products_product.sku as product_sku,
        products_product.name as product_name,
        customers_customer.name as customer_name,
        SUM(qty) as total_buy,
        SUM(total) as total_purchase

    FROM products_product
        LEFT JOIN transactions_transactiondetail ON transactions_transactiondetail.product_id = products_product.id
        LEFT JOIN transactions_transaction ON transactions_transaction.id = transactions_transactiondetail.transaction_id
        LEFT JOIN brands_brand ON brands_brand.id = products_product.brand_id
        LEFT JOIN genres_type ON genres_type.id = products_product.genre_id
        LEFT JOIN customers_customer ON transactions_transaction.customer_id = customers_customer.id
        WHERE DATE(transactions_transaction.invoice_date) >= '[first_date]' AND DATE(transactions_transaction.invoice_date) <= '[last_date]' AND transactions_transaction.typeof = 1
        GROUP BY brands_brand.name, genres_type.name, products_product.sku, products_product.name, customers_customer.name ORDER BY brands_brand.name, genres_type.name, customers_customer.name, products_product.sku, products_product.name 
    '''
    sql = sql.replace("[first_date]",str(date_first))
    sql = sql.replace("[last_date]",str(date_last))
    listData = Product.objects.raw(sql)
    return render(request, template_name, { "data" : listData })
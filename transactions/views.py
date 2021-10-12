from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from django.http import Http404  
from django.db.models import F, Q, CharField, Value
from django.db import connection
from django.urls import reverse
from django.db.models import Max
from decimal import Decimal
# Model
from transactions.models import Transaction
from transactions.models import TransactionDetail
from suppliers.models import Supplier
from customers.models import Customer
from products.models import Product

# Create your views here.

@login_required
def purchases_datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("purchases.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("purchases.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("purchases.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Transaction.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        getFilter = getData.filter(typeof = 0)
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(invoice_number__contains=searchValue) | Q(invoice_date__contains=searchValue) |  Q(supplier__name__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            t_invoice_date = F('invoice_date'),
            t_invoice_number = F('invoice_number'),
            t_supplier = F('supplier'),
            t_grandtotal = F('grandtotal'),
            t_status = F('status'),
        ).annotate(action=Value(actionButton, output_field=CharField()))
       

        response = {
            "draw":draw,
            "iTotalRecords":int(totalRecord),
            "iTotalDisplayRecords":int(totalRecordFilter),
            "aaData":list(aaData)
        }

        #print(connection.queries)

        return JsonResponse(response)

    raise Http404         

@login_required
def purchases_index(request, template_name='app/purchases/index.html'):
    return render(request, template_name)

@login_required
def purchases_create(request, template_name='app/purchases/form.html'):

    today = datetime.now().date()
    date_index = datetime.now().strftime("%Y%m%d")
    args = Transaction.objects.filter(typeof = 0) 
    args.aggregate(Max('invoice_date')) 
    getData = args.order_by('-id').first()
    invoice_number = "PRCH."+date_index+".00001"

    if getData is not None:
        invoice_number_last = getData.invoice_number.split(".")
        last_index = invoice_number_last[2]
        val = int(last_index) + 1
        next_index = str(val)
        digit = 5
        i_number = len(str(val))
        
        while digit > i_number:
            next_index = "0"+next_index
            digit -= 1

        invoice_number = "PRCH."+date_index+"."+next_index
        #return HttpResponse(invoice_number)

    tOrder = Transaction(invoice_number = invoice_number, invoice_date = today, typeof = 0, status = 0, created_at = datetime.now(), casheir_id = request.user.id)
    tOrder.save()
    lastSaved = Transaction.objects.latest('id')
    return redirect('purchases.edit', pk=lastSaved.id)

@login_required
def purchases_edit(request, pk,template_name='app/purchases/form.html'):

    transaction = get_object_or_404(Transaction, pk=pk)

    option = {
        "page_name" : "Purchase",
        "model" : transaction,
        "suppliers": Supplier.objects.order_by('name').all()
    }

    if request.method == 'POST': 

        # Get Transaction
        transaction_id = int(request.POST.get("id"))
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        
        # Get Supplier
        supplier_id = int(request.POST.get("supplier"))
        supplier = get_object_or_404(Supplier, pk=supplier_id)

        # Shopping Chart
        products = request.POST.getlist('product_id[]')
        prices = request.POST.getlist('price[]')
        qtys = request.POST.getlist('qty[]')
        totals = request.POST.getlist('total[]')
        # Reset if Exists
        TransactionDetail.objects.filter(transaction = transaction).delete()

        i = 0
        total_items = 0
        for pr in products:

            price = float(prices[i])
            qty = int(qtys[i])
            total = float(totals[i])

            product = get_object_or_404(Product, pk=pr)
            product.stock = product.stock + qty
            product.supplier = supplier
            product.save()
          
            detail = TransactionDetail(transaction = transaction, product = product, price = price, qty = qty, total = total)
            detail.save()

            i += 1
            total_items += qty

        #Update Transaction
        
        grandtotal = str(request.POST.get("grandtotal"))
        transaction.created_at = datetime.now()
        transaction.supplier = supplier
        transaction.status = 1
        transaction.total_items = total_items
        transaction.grandtotal = float(grandtotal)
        transaction.save()


        messages.success(request, 'Record updated successfully')
        return redirect('purchases.show', pk=pk)

    return render(request, template_name, option)

@login_required
def purchases_show(request, pk, template_name='app/purchases/show.html'):
    transaction = get_object_or_404(Transaction, pk=pk)
    detail = TransactionDetail.objects.filter(transaction = transaction)
    return render(request, template_name, {'transaction':transaction, "details" : detail})

@login_required
def purchases_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction:
        transaction.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('purchases.index')

@login_required
def purchases_print(request, pk, template_name='app/purchases/print.html'):
   transaction = get_object_or_404(Transaction, pk=pk)
   detail = TransactionDetail.objects.filter(transaction = transaction)
   return render(request, template_name, {'transaction':transaction, "details" : detail})

@login_required
def sales_datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("sales.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("sales.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("sales.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Transaction.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        getFilter = getData.filter(typeof = 1)
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(invoice_number__contains=searchValue) | Q(invoice_date__contains=searchValue) |  Q(customer__name__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            t_invoice_date = F('invoice_date'),
            t_invoice_number = F('invoice_number'),
            t_customer = F('customer'),
            t_grandtotal = F('grandtotal'),
            t_status = F('status'),
        ).annotate(action=Value(actionButton, output_field=CharField()))
       

        response = {
            "draw":draw,
            "iTotalRecords":int(totalRecord),
            "iTotalDisplayRecords":int(totalRecordFilter),
            "aaData":list(aaData)
        }

        #print(connection.queries)

        return JsonResponse(response)

    raise Http404         

@login_required
def sales_index(request, template_name='app/sales/index.html'):
    return render(request, template_name)

@login_required
def sales_create(request, template_name='app/sales/form.html'):

    today = datetime.now().date()
    date_index = datetime.now().strftime("%Y%m%d")
    args = Transaction.objects.filter(typeof = 1) 
    args.aggregate(Max('invoice_date')) 
    getData = args.order_by('-id').first()
    invoice_number = "SALE."+date_index+".00001"

    if getData is not None:
        invoice_number_last = getData.invoice_number.split(".")
        last_index = invoice_number_last[2]
        val = int(last_index) + 1
        next_index = str(val)
        digit = 5
        i_number = len(str(val))
        
        while digit > i_number:
            next_index = "0"+next_index
            digit -= 1

        invoice_number = "SALE."+date_index+"."+next_index
        #return HttpResponse(invoice_number)

    tOrder = Transaction(invoice_number = invoice_number, invoice_date = today, typeof = 1, status = 0, created_at = datetime.now(), casheir_id = request.user.id)
    tOrder.save()
    lastSaved = Transaction.objects.latest('id')
    return redirect('sales.edit', pk=lastSaved.id)

@login_required
def sales_edit(request, pk,template_name='app/sales/form.html'):

    transaction = get_object_or_404(Transaction, pk=pk)

    option = {
        "page_name" : "Sale",
        "model" : transaction,
        "customers": Customer.objects.order_by('name').all()
    }

    if request.method == 'POST': 

        # Get Transaction
        transaction_id = int(request.POST.get("id"))
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        
        # Get Customer
        customer_id = int(request.POST.get("customer"))
        customer = get_object_or_404(Customer, pk=customer_id)

        # Shopping Chart
        products = request.POST.getlist('product_id[]')
        prices = request.POST.getlist('price[]')
        qtys = request.POST.getlist('qty[]')
        totals = request.POST.getlist('total[]')
        # Reset if Exists
        TransactionDetail.objects.filter(transaction = transaction).delete()

        i = 0
        total_items = 0
        for pr in products:

            price = float(prices[i])
            qty = int(qtys[i])
            total = float(totals[i])

            product = get_object_or_404(Product, pk=pr)
            product.stock = product.stock - qty
            product.save()
          
            detail = TransactionDetail(transaction = transaction, product = product, price = price, qty = qty, total = total)
            detail.save()

            i += 1
            total_items += qty

        # Update Transaction
        transaction.created_at = datetime.now()
        transaction.customer = customer
        transaction.status = 1
        transaction.total_items = total_items
        transaction.subtotal = float(request.POST.get("subtotal"))
        transaction.discount = float(request.POST.get("discount"))
        transaction.tax = float(request.POST.get("tax"))
        transaction.grandtotal = float(request.POST.get("grandtotal"))
        transaction.cash = float(request.POST.get("cash"))
        transaction.change = float(request.POST.get("change"))
        transaction.save()


        messages.success(request, 'Record updated successfully')
        return redirect('sales.show', pk=pk)

    return render(request, template_name, option)

@login_required
def sales_show(request, pk, template_name='app/sales/show.html'):
    transaction = get_object_or_404(Transaction, pk=pk)
    detail = TransactionDetail.objects.filter(transaction = transaction)
    return render(request, template_name, {'transaction':transaction, "details" : detail})

@login_required
def sales_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction:
        transaction.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('sales.index')

@login_required
def sales_print(request, pk, template_name='app/sales/print.html'):
   transaction = get_object_or_404(Transaction, pk=pk)
   detail = TransactionDetail.objects.filter(transaction = transaction)
   return render(request, template_name, {'transaction':transaction, "details" : detail})
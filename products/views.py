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
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


import os
import uuid

# Model
from products.models import Product
from categories.models import Category

# Create your views here.

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'brand', 'genre',
                  'supplier', 'categories', 'stock', 'price_purchase', 'price_sales', 'price_profit', 'date_expired', 'description', 'notes', 'image']

@login_required
def select2(request):
    if request.method == 'POST':

        searchValue =  str(request.POST.get("q"))
        tp =  int(request.POST.get("type"))
        getData = Product.objects
        getDataOrder = getData.filter(stock__gte = 0)
        label_price = "price"
        if tp == 0:
            label_price = "price_purchase"
        else:
            label_price = "price_sales"

        if "q" in request.POST:
            getDataOrder = getData.filter(Q(name__contains=searchValue) | Q(sku__contains=searchValue)).order_by("name")

        row = 1
        rowperpage = 10

        aaData = getDataOrder.values(
            text = F('name'),
        ).annotate(id = F('id'), sku = F("sku"), stock = F("stock"), price = F(label_price) )

        response = list(aaData)

        return JsonResponse(response, safe=False)   


    raise Http404     


@login_required
def datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("products.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("products.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("products.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Product.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        getFilter = getData
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(name__contains=searchValue) | Q(description__contains=searchValue) | Q(
                stock__contains=searchValue) | Q(sku__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            product_name = F('name'),
            product_sku = F('sku'),
            product_stock=F('stock'),
            product_description = F('description'),
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
def index(request, template_name='app/products/index.html'):
    return render(request, template_name)


@login_required
def create(request, template_name='app/products/form.html'):
    form = ProductForm(request.POST or None)
    form.instance.date_expired = datetime.today()
    fileUpload = None
    if form.is_valid():

        if bool(request.FILES.get('file_image', False)) == True:
            myfile = request.FILES['file_image']
            fs = FileSystemStorage("static/uploads")
            ext = os.path.splitext(myfile.name)[-1]
            ruuid = str(uuid.uuid1())
            filename = fs.save(ruuid+""+ext, myfile)
            fileUpload = fs.url(filename)


        obj = form.save(commit=False)
        obj.created_at = datetime.now()
        obj.image = fileUpload
        obj.save()
        form.save_m2m()

        messages.success(request, 'Record created successfully')
        product = Product.objects.latest('id')
        return redirect('products.show', pk=product.id)
    return render(request, template_name, {'form':form, 'type': 'create', 'page_name' : 'Product'})

@login_required
def show(request, pk, template_name='app/products/show.html'):
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {'product': product})

@login_required
def edit(request, pk, template_name='app/products/form.html'):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    fileUpload = product.image
    if form.is_valid():

        if bool(request.FILES.get('file_image', False)) == True:
            file_image = request.FILES['file_image']
            product = get_object_or_404(Product, pk=pk)
            if product.image:
                os.remove(os.path.join("static/uploads", product.image))

            myfile = file_image
            fs = FileSystemStorage("static/uploads")
            ext = os.path.splitext(myfile.name)[-1]
            ruuid = str(uuid.uuid1())
            filename = fs.save(ruuid+""+ext, myfile)
            fileUpload = fs.url(filename)

        obj = form.save(commit=False)
        obj.image = fileUpload
        obj.save()
        messages.success(request, 'Record updated successfully')
        return redirect('products.show', pk=pk)

    return render(request, template_name, {'form':form, 'type': 'edit', 'page_name' : 'Product'})

@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product:

        if product.image:
            os.remove(os.path.join("static/uploads", product.image))

        product.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('products.index')

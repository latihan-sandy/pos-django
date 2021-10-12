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
# Model
from brands.models import Brand

# Create your views here.

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']


@login_required
def datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("brands.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("brands.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("brands.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Brand.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        getFilter = getData
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(name__contains=searchValue) | Q(description__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            brand_name = F('name'),
            brand_description = F('description'),
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
def index(request, template_name='app/brand/index.html'):
    return render(request, template_name)


@login_required
def create(request, template_name='app/brand/form.html'):
    form = BrandForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_at = datetime.now()
        obj.save()
        messages.success(request, 'Record created successfully')
        brand = Brand.objects.latest('id')
        return redirect('brands.show', pk=brand.id)
    return render(request, template_name, {'form':form, 'type': 'create', 'page_name' : 'Brand'})

@login_required
def show(request, pk, template_name='app/brand/show.html'):
    brand= get_object_or_404(Brand, pk=pk)
    return render(request, template_name, {'brand':brand})

@login_required
def edit(request, pk, template_name='app/brand/form.html'):
    brand= get_object_or_404(Brand, pk=pk)
    form = BrandForm(request.POST or None, instance=brand)
    if form.is_valid():
        form.save()
        messages.success(request, 'Record updated successfully')
        return redirect('brands.show', pk=pk)
    return render(request, template_name, {'form':form, 'type': 'edit', 'page_name' : 'Brand'})

@login_required
def delete(request, pk):
    brand= get_object_or_404(Brand, pk=pk)
    if brand:
        brand.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('brands.index')
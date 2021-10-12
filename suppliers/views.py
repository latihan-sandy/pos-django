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
from suppliers.models import Supplier

# Create your views here.

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'website', 'address']


@login_required
def datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("suppliers.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("suppliers.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("suppliers.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Supplier.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        getFilter = getData
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(name__contains=searchValue) | Q(phone__contains=searchValue) | Q(email__contains=searchValue) | Q(website__contains=searchValue) | Q(address__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            supplier_name = F('name'),
            supplier_email = F('email'),
            supplier_phone = F('phone'),
            supplier_website = F('website'),
            supplier_addresss = F('address'),
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
def index(request, template_name='app/supplier/index.html'):
    return render(request, template_name)


@login_required
def create(request, template_name='app/supplier/form.html'):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_at = datetime.now()
        obj.save()
        messages.success(request, 'Record created successfully')
        supplier = Supplier.objects.latest('id')
        return redirect('suppliers.show', pk=supplier.id)
    return render(request, template_name, {'form':form, 'type': 'create', 'page_name' : 'Supplier'})

@login_required
def show(request, pk, template_name='app/supplier/show.html'):
    supplier= get_object_or_404(Supplier, pk=pk)
    return render(request, template_name, {'supplier':supplier})

@login_required
def edit(request, pk, template_name='app/supplier/form.html'):
    supplier= get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request, 'Record updated successfully')
        return redirect('suppliers.show', pk=pk)
    return render(request, template_name, {'form':form, 'type': 'edit', 'page_name' : 'Supplier'})

@login_required
def delete(request, pk):
    supplier= get_object_or_404(Supplier, pk=pk)
    if supplier:
        supplier.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('suppliers.index')
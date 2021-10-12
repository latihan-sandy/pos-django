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
from genres.models import Type

# Create your views here.

class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'description']


@login_required
def datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("types.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("types.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("types.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = Type.objects
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
            type_name = F('name'),
            type_description = F('description'),
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
def index(request, template_name='app/type/index.html'):
    return render(request, template_name)


@login_required
def create(request, template_name='app/type/form.html'):
    form = TypeForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.created_at = datetime.now()
        obj.save()
        messages.success(request, 'Record created successfully')
        genre = Type.objects.latest('id')
        return redirect('types.show', pk=genre.id)
    return render(request, template_name, {'form':form, 'type': 'create', 'page_name' : 'Type'})

@login_required
def show(request, pk, template_name='app/type/show.html'):
    genre = get_object_or_404(Type, pk=pk)
    return render(request, template_name, {'type':genre})

@login_required
def edit(request, pk, template_name='app/type/form.html'):
    genre= get_object_or_404(Type, pk=pk)
    form = TypeForm(request.POST or None, instance=genre)
    if form.is_valid():
        form.save()
        messages.success(request, 'Record updated successfully')
        return redirect('types.show', pk=pk)
    return render(request, template_name, {'form':form, 'type': 'edit', 'page_name' : 'Type'})

@login_required
def delete(request, pk):
    genre = get_object_or_404(Type, pk=pk)
    if genre:
        genre.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('types.index')
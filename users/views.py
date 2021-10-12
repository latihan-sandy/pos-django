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
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.template import RequestContext
#Model
from django.contrib.auth.models import User

# Create your views here.

# forms.py
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email']

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'form-control select-multiple'


class UserChangeForm(forms.ModelForm):

    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
            help_text="Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'form-control select-multiple'

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@login_required
def datatable(request):
    if request.method == 'POST':


        ## Action Buttons ( Addtional Buttons )
        actionButton = ""
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("users.show", kwargs={'pk': 0})+"' class='btn btn-sm btn-success btn-show'><i class='fa fa-search'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("users.edit", kwargs={'pk': 0})+"' class='btn btn-sm btn-info btn-edit'><i class='fa fa-edit'></i></a>&nbsp;"
        actionButton += "<a href='javascript:void(0);' data-route='"+reverse("users.delete", kwargs={'pk': 0})+"' class='btn btn-sm btn-danger btn-delete'><i class='fa fa-trash'></i></a>"
      
        ## Read value
        draw =  int(request.POST.get("draw"))
        row =  int(request.POST.get("start"))
        rowperpage =  int(request.POST.get("length"))
        columnIndex =  request.POST.get("order[0][column]")
        columnName =   request.POST.get("columns["+columnIndex+"][name]")
        columnSortOrder =   request.POST.get("order[0][dir]")
        searchValue =  request.POST.get("search[value]")


        ## Total number of records without filtering
        getData = User.objects
        totalRecord = getData.count()

        ## Total number of records with filtering  
        ## Search
        login_id = request.user.id
        getFilter = getData.filter(~Q(id=login_id))
        
        if(searchValue !=""):
            getFilter = getData.filter(Q(username__contains=searchValue) | Q(email__contains=searchValue) | Q(first_name__contains=searchValue) | Q(last_name__contains=searchValue))
        
        totalRecordFilter = getFilter.count()
        getDataOrder =  getFilter

        if(columnSortOrder == "desc"):
            getDataOrder =  getFilter.order_by('-'+columnName)
        else:
            getDataOrder =  getFilter.order_by(columnName)

        aaData = getDataOrder[row:(row + rowperpage)].values(
            key_id = F('id'),
            user_username = F('username'),
            user_email = F('email'),
            user_is_superuser = F('is_superuser'),
            user_is_staff = F('is_staff'),
            user_is_active = F('is_active'),
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
def index(request, template_name='app/users/index.html'):
    return render(request, template_name)

@login_required
def create(request, template_name='app/users/form.html'):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Record created successfully')
        user = User.objects.latest('id')
        return redirect('users.show', pk=user.id)
    return render(request, template_name, {'form':form, 'type': 'create', 'page_name' : 'User'})


@login_required
def show(request, pk, template_name='app/users/show.html'):
    user = get_object_or_404(User, pk=pk)
    return render(request, template_name, {'user':user})

@login_required
def edit(request, pk, template_name='app/users/form.html'):
    user= get_object_or_404(User, pk=pk)
    form = UserChangeForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        form.save_m2m()
        messages.success(request, 'Record updated successfully')
        return redirect('users.show', pk=pk)
    return render(request, template_name, {'form':form, 'type': 'edit', 'page_name' : 'User'})

@login_required
def delete(request, pk):
    user= get_object_or_404(User, pk=pk)
    if user:
        user.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('users.index')

@login_required
def profile(request, template_name='app/users/profile.html'):
   id = request.user.id    
   user = User.objects.get(pk=id)
   form = UserProfileForm(request.POST or None, instance=user)
   if form.is_valid():
        form.save()
        form.save_m2m()
        messages.success(request, 'User updated successfully')
        return redirect('users.profile')
   return render(request, template_name, {'form':form, 'page_name' : 'User Profile'})

@login_required
def change_password(request, template_name='app/users/password.html'):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users.change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, template_name, {'form': form,  'page_name' : 'Change Password' })


def handler404(request, exception, template_name="app/users/404.html"):
    return render(request, template_name, status=404)


def handler500(request):
    return render(request, 'app/users/500.html', status=500)

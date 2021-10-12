"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users import views

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('', include('dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')), # new
    path('brands/', include('brands.urls')),
    path('types/', include('genres.urls')),
    path('categories/', include('categories.urls')),
    path('customers/', include('customers.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),
    path('products/', include('products.urls')),
    path('transaction/', include('transactions.urls')),
    path('reports/', include('reports.urls')),
    path('account/profile', views.profile, name='users.profile'),
    path('account/change_password', views.change_password, name='users.change_password'),
]

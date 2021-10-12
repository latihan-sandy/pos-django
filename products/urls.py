from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='products.index'),
    path('datatable', views.datatable, name='products.datatabale'),
    path('select2', views.select2, name='products.select2'),
    path('create', views.create, name='products.create'),
    path('edit/<int:pk>', views.edit, name='products.edit'),
    path('show/<int:pk>', views.show, name='products.show'),
    path('delete/<int:pk>', views.delete, name='products.delete'),
]
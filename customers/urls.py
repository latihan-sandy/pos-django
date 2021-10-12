from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='customers.index'),
    path('datatable', views.datatable, name='customers.datatabale'),
    path('create', views.create, name='customers.create'),
    path('edit/<int:pk>', views.edit, name='customers.edit'),
    path('show/<int:pk>', views.show, name='customers.show'),
    path('delete/<int:pk>', views.delete, name='customers.delete'),
]
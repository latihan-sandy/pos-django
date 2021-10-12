from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='suppliers.index'),
    path('datatable', views.datatable, name='suppliers.datatabale'),
    path('create', views.create, name='suppliers.create'),
    path('edit/<int:pk>', views.edit, name='suppliers.edit'),
    path('show/<int:pk>', views.show, name='suppliers.show'),
    path('delete/<int:pk>', views.delete, name='suppliers.delete'),
]
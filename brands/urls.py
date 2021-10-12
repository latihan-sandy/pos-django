from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='brands.index'),
    path('datatable', views.datatable, name='brands.datatabale'),
    path('create', views.create, name='brands.create'),
    path('edit/<int:pk>', views.edit, name='brands.edit'),
    path('show/<int:pk>', views.show, name='brands.show'),
    path('delete/<int:pk>', views.delete, name='brands.delete'),
]
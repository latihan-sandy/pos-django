from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='categories.index'),
    path('datatable', views.datatable, name='categories.datatabale'),
    path('create', views.create, name='categories.create'),
    path('edit/<int:pk>', views.edit, name='categories.edit'),
    path('show/<int:pk>', views.show, name='categories.show'),
    path('delete/<int:pk>', views.delete, name='categories.delete'),
]
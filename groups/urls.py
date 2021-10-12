from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='groups.index'),
    path('datatable', views.datatable, name='groups.datatabale'),
    path('create', views.create, name='groups.create'),
    path('edit/<int:pk>', views.edit, name='groups.edit'),
    path('show/<int:pk>', views.show, name='groups.show'),
    path('delete/<int:pk>', views.delete, name='groups.delete'),
]
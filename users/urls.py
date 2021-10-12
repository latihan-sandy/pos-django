from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='users.index'),
    path('datatable', views.datatable, name='users.datatabale'),
    path('create', views.create, name='users.create'),
    path('edit/<int:pk>', views.edit, name='users.edit'),
    path('show/<int:pk>', views.show, name='users.show'),
    path('delete/<int:pk>', views.delete, name='users.delete'),
]
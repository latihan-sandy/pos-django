from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='types.index'),
    path('datatable', views.datatable, name='types.datatabale'),
    path('create', views.create, name='types.create'),
    path('edit/<int:pk>', views.edit, name='types.edit'),
    path('show/<int:pk>', views.show, name='types.show'),
    path('delete/<int:pk>', views.delete, name='types.delete'),
]
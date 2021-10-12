from django.urls import path

from . import views

urlpatterns = [
    # purchase
    path('purchases', views.purchases_index, name='purchases.index'),
    path('purchases/datatable', views.purchases_datatable, name='purchases.datatabale'),
    path('purchases/create', views.purchases_create, name='purchases.create'),
    path('purchases/edit/<int:pk>', views.purchases_edit, name='purchases.edit'),
    path('purchases/show/<int:pk>', views.purchases_show, name='purchases.show'),
    path('purchases/delete/<int:pk>', views.purchases_delete, name='purchases.delete'),
    path('purchases/print/<int:pk>', views.purchases_print, name='purchases.print'),
    # sales
    path('sales', views.sales_index, name='sales.index'),
    path('sales/datatable', views.sales_datatable, name='sales.datatabale'),
    path('sales/create', views.sales_create, name='sales.create'),
    path('sales/edit/<int:pk>', views.sales_edit, name='sales.edit'),
    path('sales/show/<int:pk>', views.sales_show, name='sales.show'),
    path('sales/delete/<int:pk>', views.sales_delete, name='sales.delete'),
    path('sales/print/<int:pk>', views.sales_print, name='sales.print'),
]
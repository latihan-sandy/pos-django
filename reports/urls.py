from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='reports.index'),
    # Purchase
    path('purchase_period/<str:date_first>/<str:date_last>', views.purchase_period, name='reports.purchase_period'),
    path('purchase_supplier/<str:date_first>/<str:date_last>', views.purchase_supplier, name='reports.purchase_supplier'),
    path('purchase_product/<str:date_first>/<str:date_last>', views.purchase_product, name='reports.purchase_product'),
    # Sales
    path('sale_period/<str:date_first>/<str:date_last>', views.sale_period, name='reports.sale_period'),
    path('sale_customer/<str:date_first>/<str:date_last>', views.sale_customer, name='reports.sale_customer'),
    path('sale_product/<str:date_first>/<str:date_last>', views.sale_product, name='reports.sale_product'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard', views.index, name='dashboard.index'),
    path('dashboard/api', views.api, name='dashboard.api'),
]

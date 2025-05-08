# bulk_orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.bulk_order_list, name='bulk_order_list'),
]

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('select_payment/<int:order_id>/', views.select_payment_method, name='select_payment'),
    path('paypal_payment/<int:order_id>/', views.paypal_payment, name='paypal_payment'),
    path('gcash_payment/<int:order_id>/', views.gcash_payment, name='gcash_payment'),
    path('cod_payment/<int:order_id>/', views.cod_payment, name='cod_payment'),
    path('payment_confirmation/<int:order_id>/', views.payment_confirmation, name='payment_confirmation'),
]

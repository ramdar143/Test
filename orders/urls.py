from django.urls import path
from . import views

app_name = 'orders' 

urlpatterns = [
    path('', views.order_list, name='order_list'),  # List orders
    path('create/', views.create_order, name='create_order'),  # Create a new order
    path('order/<int:pk>/', views.order_detail, name='order_detail'),  # Order detail
    path('order/<int:pk>/update/', views.update_order, name='update_order'),  # Update order
    path('order/<int:pk>/delete/', views.delete_order, name='delete_order'),  # Delete order
    path('update-order-item/<int:item_id>/', views.update_order_item, name='update_order_item'),  # Update order item
    path('cancel-order-item/<int:item_id>/', views.cancel_order_item, name='cancel_order_item'),  # Cancel order item
    path('order-item/<int:item_id>/', views.order_item_view, name='order_item_view'),  # This URL could be renamed for clarity
    path('order/<int:pk>/confirm/', views.confirm_order, name='confirm_order'),  # Confirm order
    path('order/summary/', views.order_summary_and_payment, name='order_summary_and_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('place_order/', views.place_order, name='place_order'),
    path('my-orders/', views.order_list_customer, name='order_list_customer'),
]

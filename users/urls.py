# users/urls.py
from django.urls import path
from .views import RegisterView, CustomerRegisterView, registration_complete, access_denied
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, customer_dashboard, admin_dashboard, kitchen_dashboard, delivery_dashboard, order_manager_dashboard
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.landing_redirect, name='landing_page'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register/admin/', RegisterView.as_view(), name='admin_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('registration-complete/', registration_complete, name='registration_complete'),
    path('access-denied/', access_denied, name='access_denied'),
    path('customer-dashboard/', customer_dashboard, name='customer_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('kitchen-dashboard/', kitchen_dashboard, name='kitchen_dashboard'),
    path('delivery-dashboard/', delivery_dashboard, name='delivery_dashboard'),
    path('order-manager-dashboard/', order_manager_dashboard, name='order_manager_dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    # path('manage-order-items/<int:order_id>/', views.manage_order_items, name='manage_order_items'),
    path("manage-users/", views.manage_users, name="manage_users"),
    path('manage-users/create/', views.user_create, name='user_create'),
    path('manage-users/<int:pk>/update/', views.user_update, name='user_update'),
    path('manage-users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('kitchen-profile/', views.update_kitchen_profile, name='update_kitchen_profile'),

]

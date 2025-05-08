from django.urls import path
from . import views
from .views import customer_menu_list

app_name = 'menu'  # Make sure this matches the `redirect('menu:...')` pattern

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('create-category/', views.create_category, name='create_category'),
    path('create/', views.create_menu_item, name='create_menu_item'),
    path('update-menu-item/<int:pk>/', views.update_menu_item, name='update_menu_item'),
    path('manage/', views.manage_menu, name='manage_menu'),  # <-- ADD THIS if missing
    path('customer_menu/', customer_menu_list, name='customer_menu'),
]

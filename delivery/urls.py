from django.urls import path
from . import views

urlpatterns = [
    path('assign_delivery/<int:pk>/', views.assign_delivery, name='assign_delivery'),
    path('update_delivery/<int:pk>/', views.update_delivery, name='update_delivery'),
]

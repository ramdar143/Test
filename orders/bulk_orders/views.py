# bulk_orders/views.py
from django.shortcuts import render

def bulk_order_list(request):
    # You can replace this with actual bulk order logic later
    return render(request, 'bulk_orders/bulk_order_list.html')

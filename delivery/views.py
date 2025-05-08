# delivery/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Delivery, Order
from .forms import DeliveryForm

# View to assign and update delivery
def assign_delivery(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == "POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.order = order
            delivery.save()
            return redirect('order_detail', pk=order.pk)
        else:
            print(form.errors)  # Add this line for debugging
    else:
        form = DeliveryForm()

    return render(request, 'delivery/assign_delivery.html', {'form': form, 'order': order})

# View to update delivery status
def update_delivery(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)

    if request.method == "POST":
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=delivery.order.pk)
        else:
            print(form.errors)  # Add this line for debugging
    else:
        form = DeliveryForm(instance=delivery)

    return render(request, 'delivery/update_delivery.html', {'form': form, 'delivery': delivery})


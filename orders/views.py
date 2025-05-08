from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, OrderItemFormSet, OrderItemForm
from .models import Order, OrderItem
from menu.models import MenuItem
from payments.models import Invoice
import datetime

@login_required
def create_order(request):
    item_id = request.GET.get('item_id')
    selected_item = None
    if item_id:
        selected_item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_item_formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and order_item_formset.is_valid():
            order_data = order_form.cleaned_data
            for key, value in order_data.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    order_data[key] = value.isoformat()
            items_data = [
                {
                    **{
                        k: (v.id if hasattr(v, "id") else v)
                        for k, v in form.cleaned_data.items()
                        if k != "DELETE"
                    },
                    "DELETE": form.cleaned_data.get("DELETE", False),
                }
                for form in order_item_formset
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
            ]
            request.session['pending_order'] = {
                'order': order_data,
                'items': items_data,
            }
            return redirect('orders:order_summary_and_payment')
        else:
            messages.error(request, "There was an error with the form. Please check the details.")
    else:
        order_form = OrderForm()
        if selected_item:
            initial_data = [{'menu_item': selected_item}]
            order_item_formset = OrderItemFormSet(queryset=OrderItem.objects.none(), initial=initial_data)
        else:
            order_item_formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    menu_items = MenuItem.objects.filter(is_available=True)
    return render(request, 'orders/create_order.html', {
        'order_form': order_form,
        'order_item_formset': order_item_formset,
        'menu_items': menu_items,
        'selected_item': selected_item,
    })

@login_required
def order_summary_and_payment(request):
    pending = request.session.get('pending_order')
    if not pending:
        messages.error(request, "No pending order found.")
        return redirect('orders:create_order')
    item_ids = [item['menu_item'] for item in pending['items']]
    menu_items = {item.id: item for item in MenuItem.objects.filter(id__in=item_ids)}
    # Attach menu_item objects for display in summary
    for item in pending['items']:
        item['menu_item_obj'] = menu_items[item['menu_item']]
    return render(request, 'orders/order_summary_and_payment.html', {
        'order': pending['order'],
        'items': pending['items']
    })

@login_required
def payment_success(request):
    pending = request.session.pop('pending_order', None)
    if not pending:
        messages.error(request, "No pending order to finalize.")
        return redirect('orders:create_order')

    order_data = pending['order']
    if 'event_date' in order_data and isinstance(order_data['event_date'], str):
        order_data['event_date'] = datetime.date.fromisoformat(order_data['event_date'])
    items_data = pending['items']

    order = Order.objects.create(
        customer=request.user,
        customer_contact=order_data['customer_contact'],
        event_date=order_data['event_date'],
        event_type=order_data['event_type'],
        guest_count=order_data['guest_count'],
        status=Order.Status.COMPLETED,
        payment_status=Order.PaymentStatus.PAID
    )

    for item in items_data:
        menu_item = MenuItem.objects.get(pk=item['menu_item'])
        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=item['quantity'],
            notes=item.get('notes', "")
        )
    messages.success(request, "Order and payment successful!")
    return redirect('orders:order_detail', pk=order.id)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = order.items.all()
    is_admin = request.user.is_staff

    invoices = order.invoices.all().order_by('-created_at')  # Even cleaner!

    if request.user != order.customer and not is_admin:
        return HttpResponseForbidden("You are not authorized to view this order.")

    context = {
        'order': order,
        'order_items': order_items,
        'invoices': invoices,
    }

    if is_admin:
        return render(request, 'orders/order_detail_admin.html', context)
    else:
        return render(request, 'orders/order_detail_customer.html', context)

def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/update_order.html', {
        'form': form,
        'order': order
    })

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == 'Pending':
        order.delete()
        messages.success(request, "Order deleted successfully.")
    else:
        messages.error(request, "You can only delete orders with Pending status.")
    return redirect('orders:order_list')

@login_required
def order_list(request):
    status_filter = request.GET.get('status', None)
    payment_filter = request.GET.get('payment_status', None)

    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    if payment_filter:
        orders = orders.filter(payment_status=payment_filter)

    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def confirm_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == Order.Status.PENDING:
        order.status = Order.Status.IN_PROGRESS
        order.save()
        amount = order.guest_count * 10  # Example pricing logic
        invoice = Invoice.objects.create(
            order=order,
            amount=amount,
            status='Paid'
        )
        messages.success(request, "Order confirmed and is now in progress. Please proceed with payment.")
        return redirect('payments:select_payments', pk=invoice.pk)
    else:
        messages.error(request, "Only Pending orders can be confirmed.")
    return redirect('orders:order_list')

def order_item_view(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.save()
            formset.instance = order
            formset.save()
            return redirect('orders:order_success')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet(initial=[{'menu_item': menu_item}])
    return render(request, 'orders/order_form.html', {
        'order_form': order_form,
        'formset': formset,
        'menu_item': menu_item,
    })

@login_required
def update_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Order item updated successfully!")
            return redirect('orders:order_detail', pk=order_item.order.id)
    else:
        form = OrderItemForm(instance=order_item)
    return render(request, 'orders/update_order_item.html', {'form': form, 'order_item': order_item})

@login_required
def cancel_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    order_item.delete()
    messages.success(request, "Order item has been canceled.")
    return redirect('orders:order_detail', pk=order_item.order.id)


@login_required
def place_order(request):
    if request.method == 'POST':
        pending = request.session.pop('pending_order', None)
        if not pending:
            messages.error(request, "No pending order to finalize.")
            return redirect('orders:create_order')
        order_data = pending['order']
        # Deserialization for dates as before...
        if 'event_date' in order_data and isinstance(order_data['event_date'], str):
            order_data['event_date'] = datetime.date.fromisoformat(order_data['event_date'])
        # Create order
        order = Order.objects.create(
            customer=request.user,
            customer_contact=order_data['customer_contact'],
            event_date=order_data['event_date'],
            event_type=order_data['event_type'],
            guest_count=order_data['guest_count'],
            status='Pending'
        )
        for item in pending['items']:
            menu_item = MenuItem.objects.get(pk=item['menu_item'])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item['quantity'],
                notes=item.get('notes', '')
            )
        return redirect('payments:select_payment', order_id=order.id)
    # On GET, redirect somewhere safe:
    return redirect('orders:create_order')




@login_required
def order_list_customer(request):
    orders = request.user.orders.all().order_by('-created_at')  # Uses related_name='orders' from your model
    return render(request, 'orders/order_list_customer.html', {'orders': orders})
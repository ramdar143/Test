from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order  # Ensure that Order is imported from orders.models
from .forms import PaymentSelectionForm, PayPalPaymentForm, GCashPaymentForm
from django.contrib import messages
from payments.models import Invoice

def select_payment_method(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_form = PaymentSelectionForm(request.POST)

        if payment_form.is_valid():
            selected_method = payment_form.cleaned_data['method']
            if selected_method == 'paypal':
                return redirect('payments:paypal_payment', order_id=order.id)
            elif selected_method == 'gcash':
                return redirect('payments:gcash_payment', order_id=order.id)
            elif selected_method == 'cod':
                return redirect('payments:cod_payment', order_id=order.id)
    else:
        payment_form = PaymentSelectionForm()

    return render(request, 'payments/select_payment_method.html', {
        'payment_form': payment_form,
        'order': order,
    })


# PayPal Payment View
def paypal_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        paypal_form = PayPalPaymentForm(request.POST)
        if paypal_form.is_valid():
            # Process PayPal logic here...
            return redirect('payments:payment_confirmation', order_id=order.id)
    else:
        paypal_form = PayPalPaymentForm()

    return render(request, 'payments/paypal_payment.html', {
        'paypal_form': paypal_form,
        'order': order,
        'order_total': order.total,     # pass total for template amount display!
        'order_currency': 'PHP',        # or your currency logic
    })


# GCash Payment View
def gcash_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        gcash_form = GCashPaymentForm(request.POST)
        if gcash_form.is_valid():
            # Process GCash payment here
            return redirect('payments:payment_confirmation', order_id=order.id)
    else:
        gcash_form = GCashPaymentForm()

    return render(request, 'payments/gcash_payment.html', {
        'gcash_form': gcash_form,
        'order': order,
    })


# COD Payment View
def cod_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Since COD doesn't need a form, you can directly confirm the payment.
    # Process COD payment here
    return redirect('payments:payment_confirmation', order_id=order.id)


# Payment Confirmation View
def payment_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.payment_status != Order.PaymentStatus.PAID:
        order.payment_status = Order.PaymentStatus.PAID
        order.save()
    create_invoice_if_paid(order)
    return render(request, 'payments/payment_confirmation.html', {'order': order})



def create_invoice_if_paid(order):
    from payments.models import Invoice
    if order.payment_status == Order.PaymentStatus.PAID and not Invoice.objects.filter(order=order, status='Paid').exists():
        Invoice.objects.create(
            order=order,
            amount=order.total,
            status='Paid'
        )




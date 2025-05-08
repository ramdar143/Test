# payments/utils.py

import random
from .models import Payment

def process_dummy_payment(user, amount, payment_method):
    # Simulate the processing of payment here (this would be replaced by actual logic)
    # For example, in a real-world scenario, integrate with Stripe, PayPal, etc.
    
    # Let's assume the payment is always successful for now
    payment = Payment.objects.create(
        user=user,
        amount=amount,
        payment_method=payment_method,
        status='completed',  # Set to 'completed' for the mock payment
        transaction_id="dummy_transaction_id_123456",  # Use actual transaction ID in production
    )
    
    return payment

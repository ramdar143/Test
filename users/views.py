from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order, OrderItem
from .forms import AdminUserCreationForm, CustomerRegistrationForm, ProfileUpdateForm
from .models import Profile

User = get_user_model()


# Admin/Staff Registration View
class RegisterView(CreateView):
    form_class = AdminUserCreationForm
    template_name = 'users/register.html'
    success_url = '/users/registration-complete/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


# Customer Registration View
class CustomerRegisterView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'users/customer_register.html'
    success_url = '/users/registration-complete/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


# Registration Complete Page
def registration_complete(request):
    return render(request, 'users/registration_complete.html')


# Access Denied Page
def access_denied(request):
    return render(request, 'users/access_denied.html')


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        role_to_url = {
            'Admin': '/users/admin-dashboard/',
            'KitchenStaff': '/users/kitchen-dashboard/',
            'DeliveryStaff': '/users/delivery-dashboard/',
            'OrderManager': '/users/order-manager-dashboard/',
            'Customer': '/users/customer-dashboard/',
        }
        return role_to_url.get(self.request.user.role, '/')


# Customer Dashboard
@login_required
def customer_dashboard(request):
    user = request.user
    try:
        profile = user.profile
    except Exception:
        profile = None

    orders = Order.objects.filter(customer=user).order_by('-created_at')

    total_orders = orders.count()
    completed_orders = orders.filter(status=Order.Status.COMPLETED).count()
    pending_orders = orders.filter(status=Order.Status.PENDING).count()
    cancelled_orders = orders.filter(status=Order.Status.CANCELLED).count()

    total_spent = Invoice.objects.filter(
        order__customer=user,
        status='Paid'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Pie chart data
    status_labels = ["Completed", "Pending", "Cancelled"]
    status_counts = [completed_orders, pending_orders, cancelled_orders]

    context = {
        'user': user,
        'profile': profile,
        'orders': orders,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'cancelled_orders': cancelled_orders,
        'total_spent': total_spent,
        'status_labels': status_labels,
        'status_counts': status_counts,
    }
    return render(request, 'users/customer_dashboard.html', context)


# Cancel Order
@login_required
def cancel_order(request, order_id):
    # Ensure the order belongs to the logged-in customer
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status != Order.Status.CANCELLED:
        order.status = Order.Status.CANCELLED
        order.save()
        messages.success(request, "Your order has been canceled.")
    else:
        messages.warning(request, "This order is already canceled.")
    return redirect('users:customer_dashboard')


# Update Profile
@login_required
def update_profile(request):
    try:
        # Try to get the user's profile
        profile = request.user.profile
    except Profile.DoesNotExist:
        # If profile doesn't exist, create one
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('users:customer_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/update_profile.html', {'form': form})



from payments.models import Invoice
from django.db.models import Sum

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order
from payments.models import Invoice

from django.contrib.auth import get_user_model
from menu.models import MenuItem  # Make sure your app name is correct!

User = get_user_model()

@login_required
def admin_dashboard(request):
    stats = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status=Order.Status.PENDING).count(),
        'in_progress_orders': Order.objects.filter(status=Order.Status.IN_PROGRESS).count(),
        'completed_orders': Order.objects.filter(status=Order.Status.COMPLETED).count(),
        'cancelled_orders': Order.objects.filter(status=Order.Status.CANCELLED).count(),
        'paid_invoices': Invoice.objects.filter(status='Paid').count(),
        'unpaid_invoices': Invoice.objects.filter(status='Unpaid').count(),
        'cancelled_invoices': Invoice.objects.filter(status='Cancelled').count(),
        'total_revenue': Invoice.objects.filter(
            status='Paid',
            order__status=Order.Status.COMPLETED
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'total_users': User.objects.count(),                # NEW: total users
        'total_menu_items': MenuItem.objects.count(),       # NEW: total menu items
    }

    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:10]
    recent_invoices = Invoice.objects.select_related('order__customer').order_by('-created_at')[:10]

    card_stats = [
        {'icon': 'money-bill-wave', 'color': 'success', 'label': 'Total Revenue', 'value': f"₱{stats['total_revenue']:.2f}"},
        {'icon': 'shopping-cart', 'color': 'primary', 'label': 'Total Orders', 'value': stats['total_orders']},
        {'icon': 'clock', 'color': 'warning', 'label': 'Pending', 'value': stats['pending_orders']},
        {'icon': 'play', 'color': 'info', 'label': 'In Progress', 'value': stats['in_progress_orders']},
        {'icon': 'check-circle', 'color': 'success', 'label': 'Completed', 'value': stats['completed_orders']},
        {'icon': 'times-circle', 'color': 'secondary', 'label': 'Cancelled', 'value': stats['cancelled_orders']},
        {'icon': 'file-invoice-dollar', 'color': 'success', 'label': 'Paid Invoices', 'value': stats['paid_invoices']},
        {'icon': 'file-invoice', 'color': 'danger', 'label': 'Unpaid Invoices', 'value': stats['unpaid_invoices']},
        {'icon': 'file-invoice', 'color': 'secondary', 'label': 'Cancelled Inv.', 'value': stats['cancelled_invoices']},
        # The two new cards:
        {'icon': 'users', 'color': 'info', 'label': 'Total Users', 'value': stats['total_users']},
        {'icon': 'utensils', 'color': 'warning', 'label': 'Total Menu Items', 'value': stats['total_menu_items']},
    ]

    context = {
        'stats': stats,
        'recent_orders': recent_orders,
        'recent_invoices': recent_invoices,
        'card_stats': card_stats,
    }
    return render(request, 'users/admin_dashboard.html', context)




from django.utils import timezone
from preparation.models import PrepTask

# Kitchen Dashboard
@login_required
def kitchen_dashboard(request):
    # Only show tasks assigned to this user
    tasks = PrepTask.objects.filter(assigned_to=request.user)
    now = timezone.now()
    for task in tasks:
        task.is_overdue = task.due_time and (task.due_time < now) and (task.status != 'Done')
    return render(request, 'users/kitchen_dashboard.html', {'tasks': tasks})

@login_required
def update_kitchen_profile(request):
    user = request.user  # Get the current logged-in user
    profile = get_object_or_404(Profile, user=user)  # Fetch the Profile for the logged-in user
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)  # Include FILES if you have a file field
        if form.is_valid():
            form.save()
            return redirect('users:kitchen_dashboard')  # Redirect to the dashboard after saving
    else:
        form = ProfileUpdateForm(instance=profile)  # Load the form with current profile data
    
    return render(request, 'users/update_kitchen_profile.html', {'form': form})


# Delivery Dashboard
@login_required
def delivery_dashboard(request):
    return render(request, 'users/delivery_dashboard.html')


# Order Manager Dashboard
@login_required
def order_manager_dashboard(request):
    return render(request, 'users/order_manager_dashboard.html')


# Landing Redirect
def landing_redirect(request):
    return render(request, 'landing_page.html')


# Custom Logout
def custom_logout(request):
    logout(request)
    return redirect('users:login')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib import messages
from .forms import AdminUserCreationForm, AdminUserUpdateForm, CustomerRegistrationForm, ProfileUpdateForm
from .models import User, Profile

def admin_required(user):
    return user.is_superuser or getattr(user, 'role', None) == 'Admin'

@user_passes_test(admin_required)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'users/manage_users.html', {'users': users})

@user_passes_test(admin_required)
def user_create(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created.")
            return redirect('users:manage_users')
    else:
        form = AdminUserCreationForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Create User'})

@user_passes_test(admin_required)
@user_passes_test(admin_required)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated.")
            return redirect('users:manage_users')
    else:
        form = AdminUserUpdateForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Edit User'})

@user_passes_test(admin_required)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted.")
        return redirect('users:manage_users')
    return render(request, 'users/user_confirm_delete.html', {'user_obj': user})

@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('users:update_profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/update_profile.html', {'form': form})

def registration_complete(request):
    return render(request, 'users/registration_complete.html')




    
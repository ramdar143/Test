from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Category
from .forms import CategoryForm, MenuItemForm
from django.db.models import ProtectedError
from django.contrib import messages

# Function to check if user has an admin role
def user_is_admin(user):
    return user.role == 'Admin'  # Only allow access for users with role 'Admin'

# View to list available menu items (public access)
def menu_list(request):
    items = MenuItem.objects.all()
    categories = Category.objects.all()
    item_form = MenuItemForm()
    category_form = CategoryForm()
    return render(request, 'menu/menu_list.html', {
        'items': items,
        'categories': categories,
        'item_form': item_form,
        'category_form': category_form
    })

# View to create a new menu category (admin only)
@user_passes_test(user_is_admin)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')
    else:
        form = CategoryForm()
    return render(request, 'menu/create_category.html', {'form': form})

# View to create a new menu item (admin only)
@user_passes_test(user_is_admin)
def create_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/create_menu_item.html', {'form': form})

# View to update an existing menu item (admin only)
@user_passes_test(user_is_admin)
def update_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')
    else:
        form = MenuItemForm(instance=item)
    
    return render(request, 'menu/update_menu_item.html', {'form': form, 'item': item})

# View to manage the menu (admin only)
@user_passes_test(user_is_admin)
def manage_menu(request):
    items = MenuItem.objects.all()
    categories = Category.objects.all()
    item_form = MenuItemForm()
    category_form = CategoryForm()

    if request.method == "POST":
        try:
            if 'add_menu_item' in request.POST:
                item_form = MenuItemForm(request.POST, request.FILES)
                if item_form.is_valid():
                    item_form.save()
                    return redirect('menu:manage_menu')

            elif 'add_category' in request.POST:
                category_form = CategoryForm(request.POST)
                if category_form.is_valid():
                    category_form.save()
                    return redirect('menu:manage_menu')

            elif 'delete_item' in request.POST:
                item_id = request.POST.get('delete_item')
                MenuItem.objects.get(id=item_id).delete()
                return redirect('menu:manage_menu')

            elif 'delete_category' in request.POST:
                cat_id = request.POST.get('delete_category')
                category = Category.objects.get(id=cat_id)

                menu_items_using_category = MenuItem.objects.filter(category=category)

                if menu_items_using_category.exists():
                    messages.error(request, f"This category cannot be deleted because it is being used by {menu_items_using_category.count()} menu items.")
                else:
                    category.delete()
                    messages.success(request, "Category deleted successfully.")

                return redirect('menu:manage_menu')

        except ProtectedError:
            messages.error(request, "This item/category cannot be deleted because it is still in use.")

    context = {
        'items': items,
        'categories': categories,
        'item_form': item_form,
        'category_form': category_form,
    }
    return render(request, 'menu/manage_menu.html', context)



from django.contrib.auth.decorators import login_required
@login_required
def customer_menu_list(request):
    items = MenuItem.objects.all()
    categories = Category.objects.all()
    return render(request, 'menu/customer_menu_list.html', {
        'items': items,
        'categories': categories
    })
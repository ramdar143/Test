from django.contrib import admin
from .models import Category, MenuItem, Allergen

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('category', 'is_available', 'allergens')
    search_fields = ('name', 'description')

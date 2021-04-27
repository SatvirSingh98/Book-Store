from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'in_stock', 'price', 'slug']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']

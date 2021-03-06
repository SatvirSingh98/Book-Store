from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def all_products(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {'category': category,
               'products': products}
    return render(request, 'store/products/category.html', context)

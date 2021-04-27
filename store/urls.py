from django.urls import path

from .views import all_products, category_list, product_detail

app_name = 'store'

urlpatterns = [
    path('', all_products, name='index'),
    path('<slug:slug>', product_detail, name='product_detail'),
    path('shop/<slug:slug>', category_list, name='category_list'),
]

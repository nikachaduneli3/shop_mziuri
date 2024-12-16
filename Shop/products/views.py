from itertools import product

from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    filters = dict()

    product_name = request.GET.get('product_name')
    if product_name:
        filters['name__icontains'] = product_name

    min_price = request.GET.get('min_price')
    if min_price:
        filters['price__gt'] = min_price

    max_price = request.GET.get('max_price')
    if max_price:
        filters['price__lt'] = max_price

    address = request.GET.get('address')
    if address:
        filters['address__icontains'] = address

    category =  request.GET.get('category')
    if category:
        filters['category_id'] = category

    products = Product.objects.filter(**filters)
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products,
                                                              'categories': categories})


def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'product_detail.html', {'product': product})

from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {'products': products})


def product_detail(request):
    return render(request, 'product_detail.html')
from traceback import format_exc

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem
from .forms import ProductForm
from django.contrib import messages

def home(request):
    product_name = request.GET.get('product_name')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    in_stock = request.GET.get('in_stock')

    filters = dict()


    if product_name:
        filters['name__icontains'] = product_name

    if min_price:
        filters['price__gt'] = min_price

    if max_price:
        filters['price__lt'] = max_price

    if in_stock == 'on':
        filters['stock_qty__gt'] = 0

    if category:
        filters['category'] = category

    products = Product.objects.filter(**filters)

    categories = Category.objects.all()

    return render(request, 'home.html', {'products': products, 'categories': categories})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product Has Been Created Successfully')
            return redirect('home')

    return render(request, 'product_form.html', {'form': form})

def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product Has Been Updated Successfully')
            return redirect('home')
    return render(request, 'product_form.html', {'form': form})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.add_message(request, messages.SUCCESS, 'Product Has Been Deleted Successfully')
    return redirect('home')


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})



def add_product_to_cart(request, id ):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=id)
    cart_item, created  = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.qty += 1
        cart_item.save()
    return redirect('product_detail', id=id)
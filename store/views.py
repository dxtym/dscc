from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderCreateForm, ProductForm, RegisterForm
from .models import Category, Order, OrderItem, Product


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    return render(request, 'store/product_list.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    return render(request, 'store/product_detail.html', {'product': product})


def register(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:product_list')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('store:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'store/product_create.html', {'form': form})


@login_required
def order_create(request):
    initial = {}
    product_id = request.GET.get('product')
    if product_id:
        initial['product'] = product_id

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            order = Order.objects.create(user=request.user)
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            return redirect('store:order_detail', pk=order.pk)
    else:
        form = OrderCreateForm(initial=initial)

    return render(request, 'store/order_create.html', {'form': form})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

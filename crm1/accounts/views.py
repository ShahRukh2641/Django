from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from django.contrib import messages
from .form import *
from .filters import *
# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account is successfully created for " + username)
            return redirect('/login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or password is incorrect")
    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
@allowed_users(allows_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Out for Delivery').count()

    context = {
        'orders': orders,
        'totalOrders': total_orders,
        'deliveredOrders': delivered_orders,
        'pendingOrders': pending_orders
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    pending_orders = Order.objects.filter(status='Out for Delivery').count()

    context = {
        'orders': orders,
        'customers': customers,
        'totalCustomers': total_customers,
        'totalOrders': total_orders,
        'deliveredOrders': delivered_orders,
        'pendingOrders': pending_orders
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url="login")
@allowed_users(allows_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()


    context = {
        'form': form
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url="login")
@allowed_users(allows_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url="login")
@allowed_users(allows_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    # totalOrdersCount = Order.objects.filter(customer=pk).count() //anotherway
    # totalOrders = Order.objects.filter(customer=pk) //anotherway
    totalOrders = customer.order_set.all()
    totalOrdersCount = totalOrders.count()

    myfilter = OrderFilter(request.GET, queryset=totalOrders)
    totalOrders = myfilter.qs
    context = {
        'customer': customer,
        'totalOrdersCount': totalOrdersCount,
        'totalOrders': totalOrders,
        'myfilter': myfilter
    }
    return render(request, 'accounts/customers.html', context)


@login_required(login_url="login")
@allowed_users(allows_roles=['admin'])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
@allowed_users(allows_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
@allowed_users(allows_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        if order:
            order.delete()
            return redirect('/')
    context = {
        'order': order
    }
    return render(request, 'accounts/delete.html', context)

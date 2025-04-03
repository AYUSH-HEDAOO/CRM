from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Order, Product
from .forms import OrderForm, createUserForm, CustomerProfileForm
from .filters import OrderFilter
from django.views.decorators.csrf import csrf_exempt


from .models import *
from .decorators import unauthenticated_user,allowed_users,admin_only

# ------------------- (REGISTER & LOGIN) -------------------
@unauthenticated_user
def registerPage(request):
        form = createUserForm()
        if request.method == 'POST':
            form = createUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user}')
                return redirect('login')

        context = {'form': form}
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
                messages.info(request, "Username and password are incorrect")

        return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

# ------------------- (DASHBOARD & CUSTOMER VIEWS) -------------------

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-status')[:5]
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = Order.objects.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context = {
        'customers': customers, 'orders': orders,
        'total_customers': total_customers, 'total_orders': total_orders, 
        'delivered': delivered, 'pending': pending
    }
    return render(request, 'accounts/dashBoard.html', context)


def userPage(request):
    context= {}
    return render(request,'accounts/user.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    orderFilter = OrderFilter(request.GET, queryset=orders) 
    orders = orderFilter.qs

    context = {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'filter': orderFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customerProfile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)  

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('customerProfile')  # Ensure it reloads the updated page
    else:
        form = CustomerProfileForm(instance=customer)

    return render(request, 'accounts/customerProfile.html', {'form': form, 'customer': customer})

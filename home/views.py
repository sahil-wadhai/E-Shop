from django.shortcuts import render,redirect
from django.http import HttpResponse #manually added
from product.models import Product,Category
from .models import User,Address
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    product_list = Product.objects.all()
    category_list = Category.objects.all()
        
    context = {
        "featured_products":product_list,
        "recent_products":product_list.order_by('-created_at'),
        "categories": category_list
    }
    return render(request,"home/index.html",context)

@login_required(login_url="/login")
def show_listings(request):
    return render(request,"home/mylistings.html")

def login_view(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,email=email ,password=password)
        
        if user is not None:  
            login(request,user)
            # Redirect to a success page.
            return redirect("/shop")
        else:       
            return render(request,"home/login.html" )

    return render(request,"home/login.html" ) # Return an 'invalid login' error message.

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect("/login")

@login_required(login_url="/login")
def new_address(request):
    if request.method == "POST":
        locality=request.POST.get('locality')
        state = request.POST.get('state')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        user = request.user
        
        address = Address(locality=locality,state=state,city=city,postal_code=postal_code,user=user)
        address.save()

    return redirect("cart/checkout" )
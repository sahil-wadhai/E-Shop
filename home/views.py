from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse #manually added
from product.models import Product,Category,Brand
from .models import User,Address
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .form import ProductForm
# Create your views here.
category_list = Category.objects.all()
def sign_up(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(email=email, phone = phone, first_name=first_name,last_name=last_name,password=password)
        user.save()
        
        locality=request.POST.get('user_locality')
        state = request.POST.get('user_state')
        city = request.POST.get('user_city')
        postal_code = request.POST.get('user_postal_code')  
        if locality and state and city and postal_code:
            address = Address(locality=locality,state=state,city=city,postal_code=postal_code,user=user)
            address.save()

        return redirect("/shop")

    return render(request,"home/signup.html" )


def index(request):
    product_list = Product.objects.all()
    category_list = Category.objects.all()
        
    context = {
        "featured_products":product_list,
        "recent_products":product_list.order_by('-created_at'),
        "categories": category_list
    }
    return render(request,"home/index.html",context)


def login_view(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,email=email ,password=password)
        
        if user is not None:  
            login(request,user)
            if user.is_staff & user.is_superuser:
                return redirect("/admin")
            else:
                return redirect("/")
            
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

@login_required(login_url="/login")
def contact(request):
    return render(request,"home/contact.html" )

@login_required(login_url="/login")
def register_product(request):
    if request.method == "POST":
        user=request.user
        locality=request.POST.get('user_locality')
        state = request.POST.get('user_state')
        city = request.POST.get('user_city')
        postal_code = request.POST.get('user_postal_code')  
        address={}
        if locality and state and city and postal_code:
            address = Address(locality=locality,state=state,city=city,postal_code=postal_code,user=user)
            address.save()
        address_id = request.POST.get('address')
        address = Address.objects.get(Q(id=address_id) & Q(user=user))

        new_product = Product(owner=user,pickup_address=address)

        category_slug = request.POST.get('category')
        if(category_slug) : 
            category = Category.objects.get(slug=category_slug)
            if category: new_product.category = category

        brand_slug = request.POST.get('brand')
        if(brand_slug) : 
            brand = Brand.objects.get(slug=category_slug)
            if brand: new_product.brand = brand

        condition = request.POST.get('condition')
        if condition=="used": new_product.condition=condition
        
        form = ProductForm(request.POST,request.FILES,instance=new_product)
        if form.is_valid():
            form.save()
        return redirect("/listings")
    
    return redirect("/product_form")

@login_required(login_url="/login")
def product_form(request):
    categories= Category.objects.all()
    brands = Brand.objects.all()
    addresses = Address.objects.filter(user=request.user)
    context = {
        "categories":categories,
        "brands":brands,
        "addresses":addresses
    }

    return render(request,"home/product_form.html",context)

@login_required(login_url="/login")
def listings(request):
    products = Product.objects.filter(owner=request.user)
    context = {
        "categories":category_list,
        "products":products
    }
    return render(request,"home/mylistings.html",context)


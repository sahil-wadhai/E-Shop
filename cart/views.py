from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import User,Address
from product.models import Category,Cart
from .models import Payment,Order
from django.db.models import Avg,Count,Sum,Q
import razorpay
from eShop.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET

category_list = Category.objects.all()

@login_required(login_url="/login")
def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        "categories":category_list,
        "cart_items":cart_items
    }
    
    return render(request,"cart/cart.html",context)

@login_required(login_url="/login")
def remove_cart_item(request,cart_item_id):
    item = Cart.objects.get(id=cart_item_id)
    if(item.user==request.user):
        item.delete()
    return redirect("/cart")

@login_required(login_url="/login")
def inc_cart_item(request,cart_item_id):
    item = Cart.objects.get(id=cart_item_id)
    if(item.user==request.user and item.quantity<item.product.count):
        item.quantity = item.quantity+1
        item.save()
    return redirect("/cart")

@login_required(login_url="/login")
def dec_cart_item(request,cart_item_id):
    item = Cart.objects.get(id=cart_item_id)
    if(item.user==request.user):
        item.quantity = item.quantity-1
        if(item.quantity==0):
            item.delete()
        else:
            item.save()
        
    return redirect("/cart")

@login_required(login_url="/login")
def checkout(request):  
    cart_items = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    total_amount = 0
    shipping = 0
    for p in cart_items:
        if(p.quantity>p.product.count):
            cart_item_delete = Cart.objects.get(id=p.id) 
            cart_item_delete.delete()
        else:
            total_amount += p.quantity*p.product.price

    total_amount += shipping
    razor_amount = int(total_amount*100)

    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    DATA = {
        "amount": razor_amount,
        "currency": "INR",
        "receipt": "receipt#1"
    }

    payment_response = client.order.create(data=DATA)
    razorpay_order_id = payment_response['id']
    razorpay_payment_status = payment_response['status']

    if razorpay_payment_status=='created':
        payment = Payment(  user = request.user, 
                            razorpay_order_id=razorpay_order_id , 
                            razorpay_payment_status=razorpay_payment_status,
                            amount=total_amount
                         )
        payment.save()
    
    context = {
        "customer":request.user,
        "cart_items":cart_items,
        "total_amount":total_amount,
        "addresses":addresses,
        "razorpay_order_id" : razorpay_order_id,
        "razorpay_payment_status" : razorpay_payment_status,
        "razor_amount":razor_amount,
        "razorpay_key" : RAZORPAY_KEY_ID
    }
    return render(request,"cart/checkout.html",context)


@login_required(login_url="/login")
def place_order(request):
    if request.method=="POST":
        cart_items = Cart.objects.filter(user=request.user)
        address_id = request.POST.get('address')
        mobile = request.POST.get('mobile')
        address = Address.objects.get(Q(user=request.user) & Q(id=address_id))
        shipping=0
        for item in cart_items:
            order_amount = item.product.price*item.quantity + shipping
            if mobile and address:
                new_order = Order(customer=request.user,         
                                delivery_address=address,
                                product=item.product,
                                quantity=item.quantity,customer_mobile=mobile)
                new_order.save()
                item.delete()
            
    return redirect("/cart")

@login_required(login_url="/login")
def payment_done(request):
    pass
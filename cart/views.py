from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
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
    sub_total = 0
    shipping = 0
    platform = 0
    for item in cart_items:
        sub_total += item.product.price*item.quantity
    total = shipping+platform+sub_total
    context = {
        "categories":category_list,
        "cart_items":cart_items,
        "sub_total":sub_total,
        "shipping":shipping,
        "platform":platform,
        "total":total
    }
    
    return render(request,"cart/cart.html",context)

@login_required(login_url="/login")
def remove_cart_item(request,cart_item_id):
    item = Cart.objects.get(id=cart_item_id)
    if(item.user==request.user):
        item.delete()
    return redirect("/cart")

@login_required(login_url="/login")
def getCartSize(request):
    cart_size = Cart.objects.filter(user=request.user).count()
    return JsonResponse({"status":"success", "cart_size":cart_size})

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
    if not cart_items.exists():
        return redirect("/cart")

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
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        payment = Payment(  user = request.user, 
                            razorpay_order_id=razorpay_order_id , 
                            razorpay_payment_id=razorpay_payment_id,
                            paid=True
                         )
        payment.save()

        shipping=0
        total_amount=0
        for item in cart_items:
            order_amount = item.product.price*item.quantity + shipping
            total_amount += order_amount
            if mobile and address:
                product = item.product
                product.count -= item.quantity
                new_order = Order(customer=request.user,         
                                delivery_address=address,
                                product=item.product,
                                quantity=item.quantity,
                                customer_mobile=mobile,
                                order_amount=order_amount,
                                payment=payment)
                new_order.save()
                product.save()
                item.delete()
        
        payment.total_amount = total_amount
        payment.save()
            
    return render(request,"cart/order_confirm.html")


@login_required(login_url="/login")
def orders(request):
    orders = Order.objects.filter(customer=request.user)
    context = {
        "categories":category_list,
        "orders":orders
    }
    return render(request,"cart/orders.html",context)
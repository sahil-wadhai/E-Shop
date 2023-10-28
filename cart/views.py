from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import User
from product.models import Category,Cart

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

def checkout(request):  
    return render(request,"cart/checkout.html")
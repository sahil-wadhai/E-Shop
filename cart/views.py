from django.shortcuts import render,redirect
from django.http import HttpResponse #manually added

def show_cart(request):  
    return render(request,"cart/cart.html")

def checkout(request):  
    return render(request,"cart/checkout.html")
from django.shortcuts import render,redirect
from .models import Product,ProductImage,Category,Comment,Cart
from django.http import HttpResponse #manually added
from django.core.paginator import Paginator #for pagination
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
category_list = Category.objects.all()
def shop(request):

    product_list = Product.objects.all()
    search_query = request.GET.get("search")
    
    if(search_query):
        product_list = product_list.filter( Q(title__icontains=search_query) | 
                                            Q(detail__icontains = search_query) |
                                            Q(category__category_name__icontains = search_query) |
                                            Q(brand__brand_name__icontains= search_query) )
    
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context = {
        "products":products_page,
        "categories": category_list
    }
    return render(request,"product/shop.html",context)

def category_view(request,category_slug):
    
    category = Category.objects.get(slug=category_slug)
    product_list = Product.objects.filter(category = category)

    search_query = request.GET.get("search")
    
    if(search_query):
        product_list = product_list.filter( Q(title__icontains=search_query) | 
                                            Q(detail__icontains = search_query) |
                                            Q(category__category_name__icontains = search_query) |
                                            Q(brand__brand_name__icontains= search_query) )
        
    context = {
        'products' : product_list,
        'categories':category_list
    }
    return render(request,"product/shop.html",context)

@login_required(login_url="/login")
def product_detail(request,product_slug):
    product_detail = Product.objects.get(slug = product_slug)
    product_images = ProductImage.objects.filter(product=product_detail)
    comments_list = Comment.objects.filter(product=product_detail)
    related_products_list = Product.objects.filter(category=product_detail.category)

    paginator = Paginator(comments_list, 6)
    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)

    context = {
        "product" : product_detail,
        "images" : product_images,
        "categories":category_list,
        "comments":comments_page,
        "related_products":related_products_list
    }
    return render(request,"product/detail.html",context)

@login_required(login_url="/login")
def add_to_cart(request,product_slug):
    product = Product.objects.get(slug=product_slug)
    cart_item = Cart.objects.filter(user=request.user, product=product)
    quantity = request.GET.get("quantity")
    if(cart_item):
        cart_item[0].quantity = quantity
        cart_item[0].save()
    else:
        new_cart_item = Cart(user=request.user,product=product,quantity=quantity)
        new_cart_item.save()
    
    return redirect(f"/shop/view/{product_slug}")




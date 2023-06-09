from django.shortcuts import render,redirect
from .models import Product,ProductImage,Category
from django.http import HttpResponse #manually added
from django.core.paginator import Paginator #for pagination
from django.db.models import Q

# Create your views here.
def shop(request):

    product_list = Product.objects.all()
    search_query = request.GET.get("search")
    
    if(search_query):
        product_list = product_list.filter( Q(title__icontains=search_query) | 
                                            Q(detail__icontains = search_query) |
                                            Q(category__category_name__icontains = search_query) |
                                            Q(brand__brand_name__icontains= search_query) )
        
    category_list = Category.objects.all()
    
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
        'products' : product_list
    }
    return render(request,"product/shop.html",context)

def product_detail(request,product_slug):
    product_detail = Product.objects.get(slug = product_slug)
    product_images = ProductImage.objects.filter(product=product_detail)
    context = {
        "product" : product_detail,
        "images" : product_images
    }
    return render(request,"product/detail.html",context)

def add_to_cart(request,product_slug):
    print("product added to cart")
    return redirect(f"/{product_slug}")




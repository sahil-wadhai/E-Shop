from django.shortcuts import render,redirect
from django.http import HttpResponse #manually added
from product.models import Product,Category

# Create your views here.
def index(request):
    product_list = Product.objects.all()
    category_list = Category.objects.all()
        
    context = {
        "featured_products":product_list,
        "recent_products":product_list.order_by('-created'),
        "categories": category_list
    }
    return render(request,"home/index.html",context)

def show_listings(request):
    return render(request,"home/mylistings.html")
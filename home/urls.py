from django.urls import path,include
from home import views
urlpatterns = [
    path('', views.index,name='index'),
    path('listings/',views.show_listings,name='listings'),
    path('cart/',include('cart.urls')),
    path('/',include('product.urls')),
]
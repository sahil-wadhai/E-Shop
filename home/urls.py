from django.urls import path,include
from home import views
urlpatterns = [
    path('', views.index,name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('listings/',views.show_listings,name='listings'),
    path('cart/',include('cart.urls')),
    path('/',include('product.urls')),
]
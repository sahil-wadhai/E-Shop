from django.urls import path,include
from home import views
urlpatterns = [
    path('', views.index,name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('new_address', views.new_address,name='new_address'),
    path('product_form/', views.product_form,name='product_form'),
    path('register_product', views.register_product,name='register_product'),
    path('contact', views.contact,name='contact'),
    path('listings/',views.listings,name='listings'),
    path('cart/',include('cart.urls')),
    path('/',include('product.urls')),
]
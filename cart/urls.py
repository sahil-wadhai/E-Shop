from django.urls import path,include
from cart import views
urlpatterns = [
    path('', views.show_cart,name='cart'),
    path('checkout/', views.checkout,name='checkout'),
]
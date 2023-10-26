from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.show_cart,name='show_cart'),
    path('remove/<int:cart_item_id>', views.remove_cart_item,name='remove_cart_item'),
    path('checkout/', views.checkout,name='checkout'),
]
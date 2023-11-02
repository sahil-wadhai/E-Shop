from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.show_cart,name='show_cart'),
    path('remove/<int:cart_item_id>', views.remove_cart_item,name='remove_cart_item'),
    path('inc/<int:cart_item_id>', views.inc_cart_item,name='inc_cart_item'),
    path('dec/<int:cart_item_id>', views.dec_cart_item,name='dec_cart_item'),
    path('checkout/', views.checkout,name='checkout'),
    path('place_order/', views.place_order,name='place_order'),
    path('payment_done/', views.payment_done,name='payment_done'),
]
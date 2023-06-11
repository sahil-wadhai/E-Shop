from django.urls import path,include
from product import views
urlpatterns = [
    path('', views.shop,name='shop'),
    path('view/<slug:product_slug>/', views.product_detail,name='product_detail'),
    path('<slug:category_slug>/', views.category_view,name='category_view'),
    path('<slug:product_slug>/add', views.add_to_cart,name='add_to_cart')
]
from django.urls import path,include
from product import views
urlpatterns = [
    path('', views.shop,name='shop'),
    path('view/<slug:product_slug>/', views.product_detail,name='product_detail'),
    path('view/<slug:product_slug>/rate', views.rate_product,name='rate_product'),
    path('<slug:category_slug>/', views.category_view,name='category_view'),
    path('add/<slug:product_slug>/', views.add_to_cart,name='add_to_cart'),
]
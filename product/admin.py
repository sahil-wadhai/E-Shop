from django.contrib import admin
from product.models import Product,Category,Brand,ProductImage,Purchase,Comment,Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Purchase)
admin.site.register(Cart)
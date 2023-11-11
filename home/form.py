from django.forms import ModelForm
from product.models import Product


class ProductForm(ModelForm):
  class Meta:
      model = Product
      fields = ['title', 'price', 'detail' , 'product_image' ,'count']
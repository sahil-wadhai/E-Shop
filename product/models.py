from django.db import models
from home.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from .utils import unique_slug_generator
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=40,null=False,blank=False,unique=True)
    image = models.ImageField(upload_to='category_imgs/',null=True,blank=True)
    slug = models.SlugField(blank=True,null=True,unique=True)

    class Meta:
        verbose_name='category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
    def save(self,*args,**kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
            
        super(Category,self).save(*args,**kwargs)
    
class Product(models.Model):
    CONDITION_TYPE = (
        ("new","New"),
        ("used","Used")
    )
    RATING = (
        (0,0),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )

    title = models.CharField(max_length=40,null=False,blank=False)
    detail = models.TextField(max_length=500,null=False,blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    condition = models.CharField(max_length=10,choices=CONDITION_TYPE)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    product_image = models.ImageField(upload_to='thumbnail_imgs/',null=False,blank=False,default='product_imgs/default.png')
    product_rating = models.IntegerField(choices=RATING,null=False,default=0)

    status = models.BooleanField(null=False,blank=False,default=True) #availability
    count = models.PositiveIntegerField(null=False,blank=False,default=1)

    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT,null=True,blank=True,default=None)
    brand = models.ForeignKey('Brand', on_delete=models.SET_DEFAULT,null=True,blank=True,default=None)
    created = models.DateField(default=timezone.now)

    slug = models.SlugField(blank=True,null=True,unique=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug and self.title:
            self.slug = unique_slug_generator(self)
            
        super(Product,self).save(*args,**kwargs)
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=40,null=False,blank=False,unique=True)
    logo = models.ImageField(upload_to='brand_logos/',null=True,blank=True)

    class Meta:
        verbose_name='brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.brand_name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False,blank=False)
    product_image = models.ImageField(upload_to='product_imgs/',null=False,blank=False)

    class Meta:
        verbose_name='product_image'
        verbose_name_plural = 'product_images'

    def __str__(self):
        return self.product.title + str(self.id)
    
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False,blank=False)
    buyer= models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)

    class Meta:
        verbose_name='purchases'
        verbose_name_plural = 'purchases'

    def __str__(self):
        return self.product.title +str("-")+ str(self.buyer.id)
    

class Comment(models.Model):
    RATING = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False,blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    rating = models.IntegerField(choices=RATING,null=False)
    review = models.TextField(max_length=500,null=False,blank=False)
    created = models.DateField(default=timezone.now)
    def __str__(self):
        return self.product.title + str("-") + self.user.email

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False,blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    quantity = models.PositiveIntegerField(null=False,blank=False,default=1)

    def __str__(self):
        return self.product.title + str("-") + self.user.email

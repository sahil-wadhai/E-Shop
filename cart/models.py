from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone
from product.models import Product
from home.models import User,Address

class Payment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
  amount = models.FloatField()
  razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
  razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
  razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
  paid = models.BooleanField(default=False)

class Order(models.Model):
  STATUS = (
        ("pending","pending"),
        ("packed","packed"),
        ("shipped","shipped"),
        ("on the way","on the way"),
        ("delivered","delivered")
    )
  product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False,blank=False)
  customer = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
  quantity = models.PositiveIntegerField(null=False,blank=False,default=1)
  order_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=50,choices=STATUS,null=False,blank=False,default="pending")
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default="",null=True)
  customer_mobile = models.CharField(max_length = 10,null=False,default="")
  delivery_address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)

  @property
  def total_cost(self):
    return self.quantity*self.product.price
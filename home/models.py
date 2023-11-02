from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin , BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import date

# Create your models here.
#manually 



class UserManager(BaseUserManager):

    def create_superuser(self, email, phone, first_name, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must be assigned to is_staff=True'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must be assigned to is_staff=True'))

        if extra_fields.get('is_active') is not True:
            raise ValueError(_('superuser must be assigned to is_active=True'))

        return self.create_user(email, phone, first_name, password, **extra_fields)

    def create_user(self, email, phone, first_name, password, **extra_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        extra_fields.setdefault('is_active',True)
        email = self.normalize_email(email)
        user = self.model(email=email, phone = phone, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'), unique = True)
    first_name = models.CharField(max_length = 30,blank=True)
    last_name = models.CharField(max_length = 30,blank=True,default="")
    phone = models.CharField(max_length = 10,blank=True,default="")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name']
    objects=UserManager()

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    locality = models.CharField(max_length=100,null=False,blank=False)
    state = models.CharField(max_length=50,null=False,blank=False)
    city = models.CharField(max_length=50,null=False,blank=False)
    postal_code = models.CharField(max_length=5,null=False,blank=False)

    def __str__(self):
        return str(self.user) + " - " + str(self.postal_code)
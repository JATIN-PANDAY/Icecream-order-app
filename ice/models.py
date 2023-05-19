from django.db import models
from django.db.models import Sum
import uuid

class UserMaster(models.Model):
    email=models.EmailField(max_length=40)
    password=models.CharField(max_length=40)
    is_active=models.BooleanField(default=True)
    is_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email


class User(models.Model):
    user_id= models.ForeignKey(UserMaster,on_delete=models.CASCADE,blank=True, null=True)
    Username=models.CharField(max_length=40)
    Mobileno=models.IntegerField(null=True)
    Address=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Username


class Icecream(models.Model):
    icecream_name=models.CharField(max_length=200)
    price=models.IntegerField(default=100)
    image=models.ImageField(upload_to='icecream')
    def __str__(self):
        return self.icecream_name


class Order(models.Model):
    user_id= models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    icecream=models.CharField(max_length=60,null=True)
    price=models.CharField(max_length=60,null=True)
    order_id=models.CharField(max_length=500,null=True)
    is_paid=models.BooleanField(default=False)


class Cart(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='cart')
    is_paid=models.BooleanField(default=False)
    instamojo_id=models.CharField(max_length=500,null=True)


    def get_cart_total(self ):
        return Cartitems.objects.filter(cart = self).aggregate(Sum('icecream__price'))['icecream__price__sum']



class Cartitems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitems')
    icecream=models.ForeignKey(Icecream,on_delete=models.CASCADE,blank=True,null=True)
    



class AddCart(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    is_paid=models.BooleanField(default=False)
    icecream=models.ForeignKey(Icecream,on_delete=models.CASCADE,blank=True,null=True)







class Contact(models.Model):
    Email=models.CharField(max_length=40)
    Name=models.CharField(max_length=40)
    Textarea=models.CharField(max_length=2000)
    def __str__(self):
        return self.Name


   


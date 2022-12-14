from email.policy import default
from enum import auto
from turtle import title
from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import MinValueValidator
class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()
    


class Product(models.Model):
    # id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=250)
    slug=models.SlugField()
    description=models.TextField(null=True,blank=True)
    unit_price=models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey('Collection',on_delete=models.PROTECT)
    promotion=models.ManyToManyField(Promotion,blank=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering=['title']

class Collection(models.Model):
    title=models.CharField(max_length=250)
    feature_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering=['title']

class Customer(models.Model):
    membership_bronze='B'
    membership_silver='S'
    membership_gold='G'
    membership_choices=[
        (membership_bronze,'Bronze'),
         (membership_silver,'Silver'),
          (membership_gold,'Gold')
    ]

    first_name=models.CharField(max_length=254)
    last_name=models.CharField(max_length=254)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=254)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=membership_choices,default=membership_bronze)
    # order=models.ManyToManyField(Order,on_delete=models.PROTECT)
    def __str__(self):
        return self.first_name
    # class Meta:
    #     ordering=['first_name']

    #   def en_title(self, obj):
    #     return obj.post.get(post=obj.id, language="en")

class Order(models.Model):
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_COMPLETE='C'
    PAYMENT_STATUS_FAILED='F'
    PAYMENT_STATUS_CHOICES=[(PAYMENT_STATUS_COMPLETE,'COMPLETE'),
       (PAYMENT_STATUS_PENDING,'PENDING'),
       (PAYMENT_STATUS_FAILED,'FAILED')
    ]
    placed_at=models.DateTimeField(auto_now_add=True)
    PAYMENT_STATUS=models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)
    def __str__(self):
        return str(self.placed_at)
    

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)


class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    zip=models.CharField(max_length=254,null=True)

class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(default='profile-icon.jpg', null=True, blank=True)

    def __str__(self):
        return self.name if self.name else 'No Name'


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    TYPE = (
        ('Storable', 'Storable'),
        ('Consumable', 'Consumable'),
        ('Service', 'Service')
    )
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True, default=0.0)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    type = models.CharField(max_length=200, null=True, choices=TYPE)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Draft', 'Draft'),
        ('Out for Delivery', 'Out For Delivered'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.product.name
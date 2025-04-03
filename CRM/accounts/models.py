from django.db import models

from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Link to User
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    ) 

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True) 
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    ) 

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.product)

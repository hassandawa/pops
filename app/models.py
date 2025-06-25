########################################
# app\models.py
########################################

# app/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

class District(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=255, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='markets', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    market = models.ForeignKey(Market, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.district} - {self.market}"


class ProductInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="interested_users")
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product} - {self.email or self.phone or 'Anonymous'}"



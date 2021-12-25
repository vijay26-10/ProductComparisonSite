from typing import ChainMap
from django.db import models
from django.db.models.fields import CharField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class search(models.Model):
    product_search = models.CharField(max_length=1000)

class amazonProduct(models.Model):
   
    amzProductName = models.CharField(max_length=500, blank=True)
    amzProductPrice = models.FloatField(default=0)
    amzProductLink = models.URLField(max_length=400,blank=True)
    amzImageLink = models.CharField(max_length=300,blank=True)
    # amzProductRating = models.CharField(max_length=200)
    # amzPriceRange = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    def __str__(self):
        return self.amzProductName
class flipkartProduct(models.Model):
    flpProductName = models.CharField(max_length=500, blank=True)
    flpProductPrice = models.FloatField(default=0)
    flpProducLink = models.URLField(max_length=300,blank=True)
    flpProductImg = models.CharField(max_length=300,blank=True)
    def __str__(self):
        return self.flpProductName

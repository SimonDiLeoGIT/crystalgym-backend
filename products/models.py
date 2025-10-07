from django.db import models
from datetime import date

    
class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField()
    release_date = models.DateField(default=date.today)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Image(models.Model):
    variant = models.ForeignKey('Variant', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='variant_images/', blank=True, null=True    )
    alt_text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.variant.name}"
    
class Variant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    color = models.ForeignKey(Color, related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.name}"
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
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField()
    release_date = models.DateField(default=date.today)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

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

    # Ensure unique combination of product, color, and size
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color'],
                name='unique_product_color'
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
class VariantSize(models.Model):
    variant = models.ForeignKey(Variant, related_name='variant_sizes', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='variant_sizes', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['variant', 'size'],
                name='unique_variant_size'
            )
        ]

    def __str__(self):
        return f"{self.variant.name} - {self.size.name}"
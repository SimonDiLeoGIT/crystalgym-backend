from django.contrib import admin
from .models import Product, Category, Variant, Color, Gender, Size

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Color)
admin.site.register(Gender)
admin.site.register(Size)
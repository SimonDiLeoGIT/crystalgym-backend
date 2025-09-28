from django.contrib import admin
from .models import Product, Category, Variant, Color, Gender, Size, Image

admin.site.index_title = "Crystal Gym Admin"
admin.site.site_header = "Crystal Gym Admin"
admin.site.site_title = "Crystal Gym Admin"

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Gender)
admin.site.register(Size)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'sku', 'price', 'stock')
    inlines = [ImageInline] 
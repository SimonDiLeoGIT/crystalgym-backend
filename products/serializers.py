from rest_framework import serializers
from .models import Category, Product, Gender, Color, Size, Variant, Image

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
    
    # convert image field to URL
    # without this, it returns variant_images/filename.jpg
    # with this, it returns http://localhost:8000/media/variant_images/filename.jpg
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        return rep

class VariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    images = ImageSerializer(many=True, required=False)
    
    class Meta:
        model = Variant
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        variant = Variant.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(variant=variant, **image_data)
        return variant
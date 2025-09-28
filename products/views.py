from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Variant, Gender
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VariantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def get_categories_classified_by_gender(request):
    genders = Gender.objects.all()
    data = {gender.name: [] for gender in genders}

    categories = Category.objects.all()
    for category in categories:
        products = Product.objects.filter(category=category)
        for product in products:
            gender_name = product.gender.name
            if category.name not in data[gender_name]:
                data[gender_name].append(CategorySerializer(category).data)

    return Response(data)

@api_view(['GET'])
def get_products_by_category_gender(request, gender_id, category_id):
    products = Product.objects.filter(category_id=category_id, gender_id=gender_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

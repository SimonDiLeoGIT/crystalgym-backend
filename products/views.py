from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from .models import Category, Product, Variant, Gender
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer, GroupByColorVariantSerializer

import pprint


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

@api_view(['GET'])
def get_variants_by_category_gender(request, gender_name, category_name):
    products = Product.objects.filter(category__name__iexact=category_name, gender__name__iexact=gender_name)
    variants = Variant.objects.filter(product__in=products).prefetch_related('images')
    variants_categorized_by_colors=[]
    for variant in variants:
        formated_variant = next(
            (v for v in variants_categorized_by_colors if v['product'] == variant.product and v['color'].id == variant.color.id),
            None
        )
        if not formated_variant:
            formated_variant = {
                'product':variant.product,
                'color':variant.color,
                'image':variant.images.first(),
                'name':variant.name,
                'price':variant.price,
                'sizes':[]
            }
            variants_categorized_by_colors.append(formated_variant)
        
        formated_variant['sizes'].append({
            'size':variant.size,
            'stock':variant.stock
        })

    paginator = PageNumberPagination()
    paginator.page_size = int(request.query_params.get('page_size', 10))
    result_page = paginator.paginate_queryset(variants_categorized_by_colors, request)

    serializer = GroupByColorVariantSerializer(result_page , many=True)
    return paginator.get_paginated_response(serializer.data)
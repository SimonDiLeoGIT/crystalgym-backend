from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from .models import Category, Product, Variant, Gender
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer, VariantWithProductSerializer, ImageSerializer, GroupByColorProductSerializer

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
            if not any(c['name'] == category.name for c in data[gender_name]):
                data[gender_name].append(CategorySerializer(category).data)

    return Response(data)

@api_view(['GET'])
def get_products_by_category_gender(request, gender_name, category_name):
    if not Gender.objects.filter(name__iexact=gender_name).exists():
        return Response({"detail":"Gender not found."}, status=404)
    if not Category.objects.filter(name__iexact=category_name).exists():
        return Response({"detail":"Category not found."}, status=404)
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
                'sku':variant.sku,
                'color':variant.color,
                'image':variant.images.first(),
                'name':variant.name,
                'price':variant.product.price,
                'sizes':[],
                'category':variant.product.category.name,
            }
            variants_categorized_by_colors.append(formated_variant)
        
        variant_sizes = variant.variant_sizes.all()
        for variant_size in variant_sizes:
            formated_variant['sizes'].append({
                'size':variant_size.size.name,
                'stock':variant_size.stock
            })

    paginator = PageNumberPagination()
    paginator.page_size = int(request.query_params.get('page_size', 10))
    result_page = paginator.paginate_queryset(variants_categorized_by_colors, request)

    serializer = GroupByColorProductSerializer(result_page , many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_variant_by_sku(request, sku):
    try:
        variant = Variant.objects.get(sku=sku)
    except Variant.DoesNotExist:
        return Response({"detail":"Variant not found."}, status=404)
    
    serializer = VariantWithProductSerializer(variant)
    return Response(serializer.data)

@api_view(['GET'])
def get_variants_by_product_id(request, product_id):
    variants = Variant.objects.filter(product_id=product_id)
    
    if not variants.exists():
        return Response(
            {"detail": f"Variants not found for product with id {product_id}."},
            status=404
        )
    
    serializer = VariantSerializer(variants, many=True)

    data = serializer.data

    #  Add image field for first image
    for variant in data:
        variant_obj = variants.get(id=variant['id'])
        first_image = variant_obj.images.first()
        variant['image'] = ImageSerializer(first_image).data if first_image else None

    return Response(data)
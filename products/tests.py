from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Gender, Product, Variant, Image, Color, Size
from .serializers import VariantSerializer
from datetime import date
from django.contrib.auth.models import User

class ProductsTests(TestCase):

    def setUp(self):
        # Create test data
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Hoodies", description="All hoodies")
        self.gender = Gender.objects.create(name="Men")

        self.product1 = Product.objects.create(
            name="Hoodie 1",
            description="Cool hoodie",
            release_date=date.today(),
            category=self.category,
            gender=self.gender
        )

        # Another product with different category/gender
        other_category = Category.objects.create(name="Shirts", description="All shirts")
        other_gender = Gender.objects.create(name="Women")
        Product.objects.create(
            name="Shirt 1",
            description="Not included",
            release_date=date.today(),
            category=other_category,
            gender=other_gender
        )

        Product.objects.create(
            name="Hoodie 2",
            description="Not included",
            release_date=date.today(),
            category=self.category,
            gender=other_gender
        )
        self.color = Color.objects.create(name='red')
        self.size = Size.objects.create(name='XL')
        Variant.objects.create(
            product=self.product1,
            name='Variant Test 1',
            sku='ABC',
            color=self.color,
            size=self.size,
            price=24.56,
            stock=24,
        )

    def test_get_categories_classified_by_gender(self):
        url='/categories-by-gender/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # We expect two genders and one category in each one
        self.assertEqual(len(data), 2)
        self.assertIn('Women', data)
        self.assertIn('Men', data)
        self.assertIn('Hoodies', [cat['name'] for cat in data['Men']])
        self.assertIn('Hoodies', [cat['name'] for cat in data['Women']])

    def test_get_products_by_category_and_gender(self):
        url = f'/products/{self.gender.id}/{self.category.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # We expect only one product
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Hoodie 1')

    def test_create_variant_with_images(self):
        variant_data = {
            "product": self.product1.id,
            "name": "Hoodie 1 - Red - M",
            "sku": "HD1-RED-M",
            "color": None,
            "size": None,
            "price": "49.99",
            "stock": 100,
            "images": [
                {"alt_text": "Front view"},
                {"alt_text": "Back view"}
            ]
        }

        serializer = VariantSerializer(data=variant_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        variant = serializer.save()

        # Assertions
        self.assertEqual(Variant.objects.count(), 2)
        self.assertEqual(Image.objects.count(), 2)
        self.assertEqual(variant.name, variant_data["name"])
        self.assertEqual(variant.images.first().alt_text, "Front view")

    def test_get_variants_by_gender_and_category(self):
        url='/variants/1/1/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual('Variant Test 1', data[0]['name'])
        

    


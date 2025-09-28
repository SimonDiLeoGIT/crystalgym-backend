from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Gender, Product
from datetime import date

class GetProductsByCategoryGenderTests(TestCase):

    def setUp(self):
        # Create test data
        self.client = APIClient()

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

    


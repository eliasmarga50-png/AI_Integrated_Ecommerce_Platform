


from decimal import Decimal

from django.test import TestCase

from apps.products.filters import ProductFilter
from apps.products.models import (
    Category,
    Product,
)


class ProductFilterTest(TestCase):
    """
    Tests for ProductFilter.
    """

    @classmethod
    def setUpTestData(cls):

        cls.electronics = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        cls.fashion = Category.objects.create(
            name="Fashion",
            slug="fashion",
        )

        Product.objects.create(
            category=cls.electronics,
            name="Gaming Laptop",
            slug="gaming-laptop",
            description="Gaming laptop",
            price=Decimal("1200.00"),
            stock=10,
            is_available=True,
        )

        Product.objects.create(
            category=cls.electronics,
            name="Mechanical Keyboard",
            slug="mechanical-keyboard",
            description="Mechanical keyboard",
            price=Decimal("150.00"),
            stock=5,
            is_available=True,
        )

        Product.objects.create(
            category=cls.fashion,
            name="Leather Jacket",
            slug="leather-jacket",
            description="Premium leather jacket",
            price=Decimal("300.00"),
            stock=0,
            is_available=False,
        )

    def test_filter_by_category(self):
        """
        Filter by category.
        """
        queryset = ProductFilter(
            {
                "category": self.electronics.id,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_filter_by_name(self):
        """
        Filter by name.
        """
        queryset = ProductFilter(
            {
                "name": "Laptop",
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first().name,
            "Gaming Laptop",
        )

    def test_filter_min_price(self):
        """
        Minimum price filter.
        """
        queryset = ProductFilter(
            {
                "min_price": 500,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_filter_max_price(self):
        """
        Maximum price filter.
        """
        queryset = ProductFilter(
            {
                "max_price": 200,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_filter_price_range(self):
        """
        Price range filter.
        """
        queryset = ProductFilter(
            {
                "min_price": 100,
                "max_price": 400,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_filter_available_products(self):
        """
        Only available products.
        """
        queryset = ProductFilter(
            {
                "is_available": True,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_filter_out_of_stock(self):
        """
        Out of stock products.
        """
        queryset = ProductFilter(
            {
                "is_available": False,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_multiple_filters(self):
        """
        Multiple filters together.
        """
        queryset = ProductFilter(
            {
                "category": self.electronics.id,
                "min_price": 1000,
                "is_available": True,
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first().name,
            "Gaming Laptop",
        )

    def test_no_matching_products(self):
        """
        No matching products.
        """
        queryset = ProductFilter(
            {
                "name": "iPhone",
            },
            queryset=Product.objects.all(),
        ).qs

        self.assertEqual(
            queryset.count(),
            0,
        )



from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.products.models import Category, Product


class CategoryModelTest(TestCase):
    """
    Tests for the Category model.
    """

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

    def test_category_is_created(self):
        """
        Category should be created successfully.
        """
        self.assertEqual(
            self.category.name,
            "Electronics",
        )

    def test_category_slug(self):
        self.assertEqual(
            self.category.slug,
            "electronics",
        )

    def test_string_representation(self):
        """
        __str__ should return the category name.
        """
        self.assertEqual(
            str(self.category),
            "Electronics",
        )


class ProductModelTest(TestCase):
    """
    Tests for the Product model.
    """

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Gaming Laptop",
            slug="gaming-laptop",
            description="High-performance gaming laptop suitable for software development and gaming.",
            price=Decimal("1200.00"),
            stock=10,
            is_available=True,
        )

    def test_product_creation(self):
        """
        Product should be created successfully.
        """
        self.assertEqual(
            self.product.name,
            "Gaming Laptop",
        )

    def test_product_price(self):
        self.assertEqual(
            self.product.price,
            Decimal("1200.00"),
        )

    def test_product_stock(self):
        self.assertEqual(
            self.product.stock,
            10,
        )

    def test_product_availability(self):
        self.assertTrue(
            self.product.is_available
        )

    def test_product_category(self):
        self.assertEqual(
            self.product.category,
            self.category,
        )

    def test_product_slug(self):
        self.assertEqual(
            self.product.slug,
            "gaming-laptop",
        )

    def test_string_representation(self):
        """
        __str__ should return the product name.
        """
        self.assertEqual(
            str(self.product),
            "Gaming Laptop",
        )

    def test_price_must_be_positive(self):
        """
        Negative prices should fail model validation.
        """
        self.product.price = Decimal("-10.00")

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_stock_cannot_be_negative(self):
        """
        Negative stock should fail validation.
        """
        self.product.stock = -5

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_slug_is_not_empty(self):
        """
        Slug should not be empty.
        """
        self.product.slug = ""

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_category_relationship(self):
        """
        Product should belong to the correct category.
        """
        self.assertEqual(
            self.product.category.name,
            "Electronics",
        )

    def test_default_availability(self):
        """
        Product availability should reflect the stored value.
        """
        self.assertIsInstance(
            self.product.is_available,
            bool,
        )

    def test_product_exists_in_database(self):
        """
        Product should exist in the database.
        """
        self.assertEqual(
            Product.objects.count(),
            1,
        )

    def test_category_exists_in_database(self):
        """
        Category should exist in the database.
        """
        self.assertEqual(
            Category.objects.count(),
            1,
        )
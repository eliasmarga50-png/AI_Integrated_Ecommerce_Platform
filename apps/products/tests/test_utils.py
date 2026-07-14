


from decimal import Decimal

from django.test import TestCase

from apps.products.utils import (
    calculate_discount_price,
    calculate_tax,
    format_price,
    generate_slug,
    generate_sku,
    stock_status,
)


class ProductUtilsTest(TestCase):
    """
    Tests for utility functions.
    """

    def test_generate_slug(self):
        """
        Slug should be generated correctly.
        """
        slug = generate_slug(
            "Gaming Laptop Pro"
        )

        self.assertEqual(
            slug,
            "gaming-laptop-pro",
        )

    def test_generate_sku(self):
        """
        SKU should be generated.
        """
        sku = generate_sku(
            "Electronics",
            "Gaming Laptop",
        )

        self.assertIsInstance(
            sku,
            str,
        )

        self.assertGreater(
            len(sku),
            5,
        )

    def test_discount_price(self):
        """
        Discount calculation.
        """
        price = Decimal("1000.00")

        discounted = calculate_discount_price(
            price,
            20,
        )

        self.assertEqual(
            discounted,
            Decimal("800.00"),
        )

    def test_zero_discount(self):
        """
        Zero discount should
        keep original price.
        """
        price = Decimal("500.00")

        discounted = calculate_discount_price(
            price,
            0,
        )

        self.assertEqual(
            discounted,
            Decimal("500.00"),
        )

    def test_full_discount(self):
        """
        100% discount.
        """
        price = Decimal("500.00")

        discounted = calculate_discount_price(
            price,
            100,
        )

        self.assertEqual(
            discounted,
            Decimal("0.00"),
        )

    def test_tax_calculation(self):
        """
        Tax calculation.
        """
        price = Decimal("1000.00")

        taxed = calculate_tax(
            price,
            15,
        )

        self.assertEqual(
            taxed,
            Decimal("1150.00"),
        )

    def test_format_price(self):
        """
        Price formatting.
        """
        formatted = format_price(
            Decimal("1200.50")
        )

        self.assertEqual(
            formatted,
            "1,200.50",
        )

    def test_stock_available(self):
        """
        Stock available.
        """
        status = stock_status(10)

        self.assertEqual(
            status,
            "In Stock",
        )

    def test_stock_low(self):
        """
        Low stock.
        """
        status = stock_status(3)

        self.assertEqual(
            status,
            "Low Stock",
        )

    def test_stock_empty(self):
        """
        Out of stock.
        """
        status = stock_status(0)

        self.assertEqual(
            status,
            "Out of Stock",
        )



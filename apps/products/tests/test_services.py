


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import (
    Category,
    Product,
)
from apps.products.forms import ProductForm
from apps.products.services import ProductService


User = get_user_model()


class ProductServiceTest(TestCase):
    """
    Tests for ProductService.
    """

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        cls.product = Product.objects.create(
            category=cls.category,
            name="Gaming Laptop",
            slug="gaming-laptop",
            description=(
                "High performance laptop "
                "for software developers."
            ),
            price=Decimal("1200.00"),
            stock=10,
            is_available=True,
        )

    def valid_form(self):
        """
        Returns a valid ProductForm.
        """
        return ProductForm(
            data={
                "category": self.category.pk,
                "name": "Mechanical Keyboard",
                "description": (
                    "Professional mechanical "
                    "keyboard for programmers."
                ),
                "price": Decimal("150.00"),
                "stock": 25,
                "is_available": True,
            }
        )

    def test_get_product(self):
        """
        Service should return a product by slug.
        """
        product = ProductService.get_product(
            "gaming-laptop"
        )

        self.assertEqual(
            product.name,
            "Gaming Laptop",
        )

    def test_create_product(self):
        """
        Service should create a product.
        """
        form = self.valid_form()

        self.assertTrue(form.is_valid())

        product = ProductService.create_product(
            form
        )

        self.assertEqual(
            product.name,
            "Mechanical Keyboard"
        )

        self.assertEqual(
            Product.objects.count(),
            2,
        )

    def test_update_product(self):
        """
        Service should update product.
        """
        form = ProductForm(
            data={
                "category": self.category.pk,
                "name": "Updated Laptop",
                "description": self.product.description,
                "price": Decimal("1350.00"),
                "stock": 8,
                "is_available": True,
            },
            instance=self.product,
        )

        self.assertTrue(form.is_valid())

        product = ProductService.update_product(
            form
        )

        self.assertEqual(
            product.name,
            "Updated Laptop",
        )

        self.assertEqual(
            product.price,
            Decimal("1350.00"),
        )

    def test_delete_product(self):
        """
        Service should delete product.
        """
        ProductService.delete_product(
            self.product
        )

        self.assertEqual(
            Product.objects.count(),
            0,
        )

    def test_available_products(self):
        """
        Only available products should
        be returned.
        """
        queryset = (
            ProductService.available_products()
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_search_products(self):
        """
        Search should find products.
        """
        queryset = (
            ProductService.search_products(
                "Laptop"
            )
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_update_stock(self):
        """
        Stock should decrease.
        """
        ProductService.update_stock(
            self.product,
            3,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            7,
        )

    def test_restock_product(self):
        """
        Stock should increase.
        """
        ProductService.restock_product(
            self.product,
            5,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            15,
        )

    def test_zero_stock_marks_unavailable(self):
        """
        Product becomes unavailable
        when stock reaches zero.
        """
        ProductService.update_stock(
            self.product,
            10,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            0,
        )

        self.assertFalse(
            self.product.is_available
        )

    def test_negative_quantity_not_allowed(self):
        """
        Negative quantities
        should raise ValueError.
        """
        with self.assertRaises(
            ValueError
        ):
            ProductService.update_stock(
                self.product,
                -1,
            )

    def test_cannot_sell_more_than_stock(self):
        """
        Selling more than available
        stock should fail.
        """
        with self.assertRaises(
            ValueError
        ):
            ProductService.update_stock(
                self.product,
                100,
            )

    def test_positive_restock_required(self):
        """
        Restock quantity must
        be positive.
        """
        with self.assertRaises(
            ValueError
        ):
            ProductService.restock_product(
                self.product,
                0,
            )
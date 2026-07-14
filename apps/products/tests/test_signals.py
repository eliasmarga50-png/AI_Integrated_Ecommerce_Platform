


from decimal import Decimal

from django.test import TestCase

from apps.products.models import (
    Category,
    Product,
)


class ProductSignalTest(TestCase):
    """
    Tests for Product signals.
    """

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

    def create_product(
        self,
        name="Gaming Laptop",
        stock=10,
    ):
        """
        Helper method to create products.
        """
        return Product.objects.create(
            category=self.category,
            name=name,
            description=(
                "Professional gaming laptop "
                "for developers."
            ),
            price=Decimal("1200.00"),
            stock=stock,
            is_available=True,
        )

    # -----------------------------------------
    # PRE SAVE SIGNALS
    # -----------------------------------------

    def test_slug_generated(self):
        """
        Slug should be automatically generated.
        """
        product = self.create_product()

        self.assertEqual(
            product.slug,
            "gaming-laptop",
        )

    def test_product_available_when_stock_positive(self):
        """
        Product should be available.
        """
        product = self.create_product(
            stock=5,
        )

        self.assertTrue(
            product.is_available
        )

    def test_product_unavailable_when_stock_zero(self):
        """
        Zero stock should make
        product unavailable.
        """
        product = self.create_product(
            stock=0,
        )

        self.assertFalse(
            product.is_available
        )

    def test_slug_updates_for_new_product_name(self):
        """
        Slug should match product name.
        """
        product = self.create_product(
            name="Mechanical Keyboard"
        )

        self.assertEqual(
            product.slug,
            "mechanical-keyboard",
        )

    # -----------------------------------------
    # POST SAVE SIGNALS
    # -----------------------------------------

    def test_product_created(self):
        """
        Product should exist
        after save.
        """
        self.create_product()

        self.assertEqual(
            Product.objects.count(),
            1,
        )

    def test_multiple_products_created(self):
        """
        Multiple products should
        save successfully.
        """
        self.create_product()

        self.create_product(
            name="Gaming Mouse"
        )

        self.assertEqual(
            Product.objects.count(),
            2,
        )

    # -----------------------------------------
    # UPDATE SIGNALS
    # -----------------------------------------

    def test_stock_update_changes_availability(self):
        """
        Availability should update
        after stock change.
        """
        product = self.create_product(
            stock=5,
        )

        product.stock = 0
        product.save()

        product.refresh_from_db()

        self.assertFalse(
            product.is_available
        )

    def test_name_update_keeps_valid_slug(self):
        """
        Slug should remain valid after
        name update.
        """
        product = self.create_product()

        product.name = "Business Laptop"
        product.slug = ""

        product.save()

        product.refresh_from_db()

        self.assertEqual(
            product.slug,
            "business-laptop",
        )

    # -----------------------------------------
    # DELETE SIGNALS
    # -----------------------------------------

    def test_product_deleted(self):
        """
        Product deletion.
        """
        product = self.create_product()

        product.delete()

        self.assertEqual(
            Product.objects.count(),
            0,
        )

    # -----------------------------------------
    # DATABASE CONSISTENCY
    # -----------------------------------------

    def test_product_saved_once(self):
        """
        Product should exist once.
        """
        self.create_product()

        self.assertEqual(
            Product.objects.filter(
                name="Gaming Laptop"
            ).count(),
            1,
        )

    def test_multiple_signal_operations(self):
        """
        Signals should work for
        multiple products.
        """
        for i in range(5):
            self.create_product(
                name=f"Laptop {i}"
            )

        self.assertEqual(
            Product.objects.count(),
            5,
        )

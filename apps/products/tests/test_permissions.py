


from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from apps.products.permissions import ProductPermission


User = get_user_model()


class ProductPermissionTest(TestCase):
    """
    Tests for ProductPermission.
    """

    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create_user(
    username="customer",
    email="customer@example.com",
    password="password123",
)

        cls.staff = User.objects.create_user(
            username="staff",
            email="emai1234stad",
            password="password123",
            is_staff=True,
        )

        cls.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )

    # -------------------------------------------------
    # Authentication
    # -------------------------------------------------

    def test_authenticated_user(self):
        self.assertTrue(
            ProductPermission.is_authenticated(
                self.customer
            )
        )

    def test_staff_user(self):
        self.assertTrue(
            ProductPermission.is_staff(
                self.staff
            )
        )

    def test_superuser(self):
        self.assertTrue(
            ProductPermission.is_superuser(
                self.superuser
            )
        )

    # -------------------------------------------------
    # Viewing Products
    # -------------------------------------------------

    def test_everyone_can_view_products(self):
        self.assertTrue(
            ProductPermission.can_view_products(
                self.customer
            )
        )

    def test_everyone_can_view_product_details(self):
        self.assertTrue(
            ProductPermission.can_view_product_details(
                self.customer
            )
        )

    # -------------------------------------------------
    # Reviews
    # -------------------------------------------------

    def test_customer_can_review(self):
        self.assertTrue(
            ProductPermission.can_review_product(
                self.customer
            )
        )

    # -------------------------------------------------
    # Create Product
    # -------------------------------------------------

    def test_customer_cannot_create_product(self):
        self.assertFalse(
            ProductPermission.can_create_product(
                self.customer
            )
        )

    def test_staff_can_create_product(self):
        self.assertTrue(
            ProductPermission.can_create_product(
                self.staff
            )
        )

    def test_superuser_can_create_product(self):
        self.assertTrue(
            ProductPermission.can_create_product(
                self.superuser
            )
        )

    # -------------------------------------------------
    # Update Product
    # -------------------------------------------------

    def test_customer_cannot_update(self):
        self.assertFalse(
            ProductPermission.can_update_product(
                self.customer
            )
        )

    def test_staff_can_update(self):
        self.assertTrue(
            ProductPermission.can_update_product(
                self.staff
            )
        )

    # -------------------------------------------------
    # Delete Product
    # -------------------------------------------------

    def test_customer_cannot_delete(self):
        self.assertFalse(
            ProductPermission.can_delete_product(
                self.customer
            )
        )

    def test_staff_cannot_delete(self):
        self.assertFalse(
            ProductPermission.can_delete_product(
                self.staff
            )
        )

    def test_superuser_can_delete(self):
        self.assertTrue(
            ProductPermission.can_delete_product(
                self.superuser
            )
        )

    # -------------------------------------------------
    # Inventory
    # -------------------------------------------------

    def test_staff_can_manage_inventory(self):
        self.assertTrue(
            ProductPermission.can_manage_inventory(
                self.staff
            )
        )

    def test_customer_cannot_manage_inventory(self):
        self.assertFalse(
            ProductPermission.can_manage_inventory(
                self.customer
            )
        )

    # -------------------------------------------------
    # Featured Products
    # -------------------------------------------------

    def test_only_superuser_can_feature_product(self):
        self.assertTrue(
            ProductPermission.can_feature_product(
                self.superuser
            )
        )

        self.assertFalse(
            ProductPermission.can_feature_product(
                self.staff
            )
        )

        self.assertFalse(
            ProductPermission.can_feature_product(
                self.customer
            )
        )

    # -------------------------------------------------
    # Permission Exception
    # -------------------------------------------------

    def test_require_raises_permission_denied(self):
        with self.assertRaises(
            PermissionDenied
        ):
            ProductPermission.require(
                False
            )

    def test_require_passes(self):
        try:
            ProductPermission.require(True)
        except PermissionDenied:
            self.fail(
                "PermissionDenied was raised unexpectedly."
            )

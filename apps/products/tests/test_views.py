


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.products.models import Category, Product


User = get_user_model()


class ProductViewsTest(TestCase):
    """
    Tests for Product views.
    """

    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create_user(
            username="customer",
            password="password123",
        )

        cls.staff = User.objects.create_user(
            username="staff",
            password="password123",
            is_staff=True,
        )

        cls.superuser = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@example.com",
        )

        cls.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        cls.product = Product.objects.create(
            category=cls.category,
            name="Gaming Laptop",
            slug="gaming-laptop",
            description="High-performance laptop for gaming and development.",
            price=Decimal("1200.00"),
            stock=15,
            is_available=True,
        )

    def test_product_list_page(self):
        """
        Product list page should load.
        """
        response = self.client.get(
            reverse("products:list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_product_detail_page(self):
        """
        Product detail page should load.
        """
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={
                    "slug": self.product.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_create_requires_staff(self):
        """
        Anonymous users should not create products.
        """
        response = self.client.get(
            reverse("products:create")
        )

        self.assertNotEqual(
            response.status_code,
            200,
        )

    def test_staff_can_access_create(self):
        """
        Staff members can access create page.
        """
        self.client.login(
            username="staff",
            password="password123",
        )

        response = self.client.get(
            reverse("products:create")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_customer_cannot_create(self):
        """
        Customers cannot access create page.
        """
        self.client.login(
            username="customer",
            password="password123",
        )

        response = self.client.get(
            reverse("products:create")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_staff_can_update(self):
        """
        Staff members can update products.
        """
        self.client.login(
            username="staff",
            password="password123",
        )

        response = self.client.get(
            reverse(
                "products:update",
                kwargs={
                    "slug": self.product.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_customer_cannot_update(self):
        """
        Customers cannot update products.
        """
        self.client.login(
            username="customer",
            password="password123",
        )

        response = self.client.get(
            reverse(
                "products:update",
                kwargs={
                    "slug": self.product.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_superuser_can_delete(self):
        """
        Superuser can delete products.
        """
        self.client.login(
            username="admin",
            password="admin123",
        )

        response = self.client.get(
            reverse(
                "products:delete",
                kwargs={
                    "slug": self.product.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_non_existing_product(self):
        """
        Unknown product should return 404.
        """
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={
                    "slug": "unknown-product",
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )



from decimal import Decimal

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import Category, Product
from apps.reviews.admin import ReviewAdmin
from apps.reviews.models import Review


User = get_user_model()


class MockRequest:
    """Simple mock request object."""
    pass


class ReviewAdminTests(TestCase):
    """
    Tests for the Review admin configuration.
    """

    def setUp(self):
        self.site = AdminSite()

        self.admin = ReviewAdmin(
            Review,
            self.site,
        )

        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="password123",
        )

        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            slug="laptop",
            description="Gaming Laptop",
            price=Decimal("1500.00"),
            stock=5,
        )

        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Fantastic product!",
        )

    # --------------------------------------------------
    # Admin Registration
    # --------------------------------------------------

    def test_model_registered(self):
        self.assertEqual(
            self.admin.model,
            Review,
        )

    # --------------------------------------------------
    # List Display
    # --------------------------------------------------

    def test_list_display(self):
        expected = (
            "product",
            "user",
            "rating",
            "is_edited",
            "created_at",
        )

        self.assertEqual(
            self.admin.list_display,
            expected,
        )

    # --------------------------------------------------
    # Search Fields
    # --------------------------------------------------

    def test_search_fields(self):
        expected = (
            "title",
            "comment",
            "user__username",
            "product__name",
        )

        self.assertEqual(
            self.admin.search_fields,
            expected,
        )

    # --------------------------------------------------
    # List Filter
    # --------------------------------------------------

    def test_list_filter(self):
        expected = (
            "rating",
            "is_edited",
            "created_at",
        )

        self.assertEqual(
            self.admin.list_filter,
            expected,
        )

    # --------------------------------------------------
    # Ordering
    # --------------------------------------------------

    def test_ordering(self):
        self.assertEqual(
            self.admin.ordering,
            ("-created_at",),
        )

    # --------------------------------------------------
    # Readonly Fields
    # --------------------------------------------------

    def test_readonly_fields(self):
        expected = (
            "created_at",
            "updated_at",
        )

        self.assertEqual(
            self.admin.readonly_fields,
            expected,
        )

    # --------------------------------------------------
    # Queryset
    # --------------------------------------------------

    def test_get_queryset(self):
        queryset = self.admin.get_queryset(
            MockRequest()
        )

        self.assertEqual(
            queryset.count(),
            1,
        )



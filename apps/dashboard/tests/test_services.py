


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.dashboard.services import DashboardService
from apps.products.models import Category, Product
from apps.shops.models import Shop


User = get_user_model()


class DashboardServiceTests(TestCase):

    def setUp(self):
        self.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="StrongPassword123",
            role=User.Role.SELLER,
        )

        self.other_seller = User.objects.create_user(
            username="other_seller",
            email="other@example.com",
            password="StrongPassword123",
            role=User.Role.SELLER,
        )

        self.shop = Shop.objects.create(
            owner=self.seller,
            name="Seller Shop",
        )

        self.other_shop = Shop.objects.create(
            owner=self.other_seller,
            name="Other Shop",
        )

        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

    def create_product(self, name, shop):
        return Product.objects.create(
            category=self.category,
            shop=shop,
            name=name,
            slug=name.lower().replace(" ", "-"),
            description="Test product",
            price=Decimal("100.00"),
            stock=10,
            is_available=True,
        )

    def test_seller_products_are_returned(self):
        product = self.create_product(
            "Seller Laptop",
            self.shop,
        )

        products = DashboardService._get_products(
            self.shop
        )

        self.assertIn(
            product,
            products,
        )

    def test_products_from_other_shops_are_excluded(self):
        own_product = self.create_product(
            "Own Laptop",
            self.shop,
        )

        other_product = self.create_product(
            "Other Laptop",
            self.other_shop,
        )

        products = DashboardService._get_products(
            self.shop
        )

        self.assertIn(
            own_product,
            products,
        )

        self.assertNotIn(
            other_product,
            products,
        )

    def test_missing_shop_returns_empty_queryset(self):
        products = DashboardService._get_products(
            None
        )

        self.assertEqual(
            products.count(),
            0,
        )



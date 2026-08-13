


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.shops.models import Shop


User = get_user_model()


class SellerDashboardViewTests(TestCase):
    """
    Tests for the seller dashboard view.
    """

    def setUp(self):
        self.seller = User.objects.create_user(
            username="seller_view",
            email="seller_view@example.com",
            password="StrongPassword123",
            role=User.Role.SELLER,
        )

        self.other_seller = User.objects.create_user(
            username="other_seller_view",
            email="other_seller_view@example.com",
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

    def test_seller_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard:seller_dashboard")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_seller_can_access_dashboard(self):
        self.client.force_login(self.seller)

        response = self.client.get(
            reverse("dashboard:seller_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_seller_dashboard_uses_correct_template(self):
        self.client.force_login(self.seller)

        response = self.client.get(
            reverse("dashboard:seller_dashboard")
        )

        self.assertTemplateUsed(
            response,
            "dashboard/seller/dashboard.html",
        )

    def test_seller_dashboard_contains_shop(self):
        self.client.force_login(self.seller)

        response = self.client.get(
            reverse("dashboard:seller_dashboard")
        )

        self.assertEqual(
            response.context["shop"],
            self.shop,
        )

    def test_customer_cannot_access_seller_dashboard(self):
        customer = User.objects.create_user(
            username="customer_view",
            email="customer_view@example.com",
            password="StrongPassword123",
            role=User.Role.CUSTOMER,
        )

        self.client.force_login(customer)

        response = self.client.get(
            reverse("dashboard:seller_dashboard")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_admin_cannot_access_seller_dashboard(self):
        admin = User.objects.create_user(
            username="admin_view",
            email="admin_view@example.com",
            password="StrongPassword123",
            role=User.Role.ADMIN,
        )

        self.client.force_login(admin)

        response = self.client.get(
            reverse("dashboard:seller_dashboard")
        )

        self.assertEqual(
            response.status_code,
            403,
        )




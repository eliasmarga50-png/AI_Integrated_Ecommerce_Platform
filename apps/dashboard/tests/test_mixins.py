



from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from apps.dashboard.mixins import (
    AdminRequiredMixin,
    CustomerRequiredMixin,
    SellerRequiredMixin,
)


User = get_user_model()


class DashboardPermissionMixinTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPassword123",
            role=User.Role.CUSTOMER,
        )

        self.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="StrongPassword123",
            role=User.Role.SELLER,
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="StrongPassword123",
            role=User.Role.ADMIN,
        )

    def test_customer_mixin_accepts_customer(self):
        request = self.factory.get("/dashboard/")
        request.user = self.customer

        mixin = CustomerRequiredMixin()
        mixin.request = request

        self.assertTrue(mixin.test_func())

    def test_seller_mixin_accepts_seller(self):
        request = self.factory.get("/dashboard/")
        request.user = self.seller

        mixin = SellerRequiredMixin()
        mixin.request = request

        self.assertTrue(mixin.test_func())

    def test_admin_mixin_accepts_admin(self):
        request = self.factory.get("/dashboard/")
        request.user = self.admin

        mixin = AdminRequiredMixin()
        mixin.request = request

        self.assertTrue(mixin.test_func())

    def test_customer_cannot_access_seller_dashboard(self):
        request = self.factory.get("/dashboard/")
        request.user = self.customer

        mixin = SellerRequiredMixin()
        mixin.request = request

        self.assertFalse(mixin.test_func())

    def test_seller_cannot_access_admin_dashboard(self):
        request = self.factory.get("/dashboard/")
        request.user = self.seller

        mixin = AdminRequiredMixin()
        mixin.request = request

        self.assertFalse(mixin.test_func())

    def test_admin_cannot_access_customer_dashboard(self):
        request = self.factory.get("/dashboard/")
        request.user = self.admin

        mixin = CustomerRequiredMixin()
        mixin.request = request

        self.assertFalse(mixin.test_func())



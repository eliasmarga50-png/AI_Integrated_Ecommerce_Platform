

from django.test import TestCase
from django.contrib.auth import get_user_model

from .services import UserService
from .permissions import (
    is_admin,
    is_customer,
    is_seller,
)
from .utils import normalize_email

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_customer(self):
        user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123",
        )

        self.assertEqual(
            user.role,
            User.Role.CUSTOMER,
        )

        self.assertTrue(
            user.check_password(
                "StrongPassword123"
            )
        )


class UserServiceTest(TestCase):

    def test_service_creates_user(self):

        user = UserService.create_user(
            username="john",
            email="JOHN@Example.COM",
            password="Password123",
            first_name="John",
            last_name="Doe",
        )

        self.assertEqual(
            user.username,
            "john",
        )

        self.assertTrue(
            user.check_password(
                "Password123"
            )
        )


class PermissionTest(TestCase):

    def test_customer_permission(self):

        user = User.objects.create_user(
            username="customer",
            email="customer@test.com",
            password="Password123",
        )

        self.assertTrue(
            is_customer(user)
        )

        self.assertFalse(
            is_admin(user)
        )

        self.assertFalse(
            is_seller(user)
        )


class UtilityTest(TestCase):

    def test_email_normalization(self):

        email = normalize_email(
            "ADMIN@Example.COM "
        )

        self.assertEqual(
            email,
            "admin@example.com",
        )
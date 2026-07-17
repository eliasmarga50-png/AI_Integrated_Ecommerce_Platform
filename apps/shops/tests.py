


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Shop
from .services import ShopService
from .utils import (
    generate_shop_slug,
    get_shop_display_name,
    is_shop_active,
)


User = get_user_model()


class ShopModelTests(TestCase):
    """
    Tests for the Shop model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123",
        )

    def test_shop_creation(self):
        shop = Shop.objects.create(
            owner=self.user,
            name="Elias Electronics",
        )

        self.assertEqual(
            shop.name,
            "Elias Electronics",
        )

        self.assertEqual(
            shop.owner,
            self.user,
        )

        self.assertTrue(
            shop.is_active,
        )

    def test_shop_slug_is_generated(self):
        shop = Shop.objects.create(
            owner=self.user,
            name="Elias Electronics",
        )

        self.assertEqual(
            shop.slug,
            "elias-electronics",
        )

    def test_shop_string_representation(self):
        shop = Shop.objects.create(
            owner=self.user,
            name="Elias Electronics",
        )

        self.assertEqual(
            str(shop),
            "Elias Electronics",
        )


class ShopServiceTests(TestCase):
    """
    Tests for shop business logic.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123",
        )

    def test_create_shop(self):
        shop = ShopService.create_shop(
            owner=self.user,
            name="Elias Electronics",
            description="Quality electronics",
        )

        self.assertEqual(
            shop.owner,
            self.user,
        )

        self.assertEqual(
            shop.name,
            "Elias Electronics",
        )

        self.assertTrue(
            Shop.objects.filter(
                name="Elias Electronics"
            ).exists()
        )

    def test_update_shop(self):
        shop = ShopService.create_shop(
            owner=self.user,
            name="Old Shop Name",
        )

        updated_shop = ShopService.update_shop(
            shop=shop,
            name="New Shop Name",
            description="Updated description",
        )

        self.assertEqual(
            updated_shop.name,
            "New Shop Name",
        )

        self.assertEqual(
            updated_shop.description,
            "Updated description",
        )

    def test_deactivate_shop(self):
        shop = ShopService.create_shop(
            owner=self.user,
            name="Elias Electronics",
        )

        ShopService.deactivate_shop(
            shop=shop
        )

        shop.refresh_from_db()

        self.assertFalse(
            shop.is_active
        )

    def test_activate_shop(self):
        shop = ShopService.create_shop(
            owner=self.user,
            name="Elias Electronics",
        )

        ShopService.deactivate_shop(
            shop=shop
        )

        ShopService.activate_shop(
            shop=shop
        )

        shop.refresh_from_db()

        self.assertTrue(
            shop.is_active
        )


class ShopUtilsTests(TestCase):
    """
    Tests for shop utility functions.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123",
        )

        self.shop = Shop.objects.create(
            owner=self.user,
            name="Elias Electronics",
        )

    def test_generate_shop_slug(self):
        slug = generate_shop_slug(
            "Elias Electronics"
        )

        self.assertEqual(
            slug,
            "elias-electronics",
        )

    def test_active_shop_display_name(self):
        display_name = get_shop_display_name(
            self.shop
        )

        self.assertEqual(
            display_name,
            "Elias Electronics",
        )

    def test_inactive_shop_display_name(self):
        self.shop.is_active = False
        self.shop.save()

        display_name = get_shop_display_name(
            self.shop
        )

        self.assertEqual(
            display_name,
            "Elias Electronics (Inactive)",
        )

    def test_is_shop_active(self):
        self.assertTrue(
            is_shop_active(self.shop)
        )

        self.shop.is_active = False
        self.shop.save()

        self.assertFalse(
            is_shop_active(self.shop)
        )


class ShopViewTests(TestCase):
    """
    Tests for shop views.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123",
        )

        self.other_user = User.objects.create_user(
            username="abebe",
            email="abebe@example.com",
            password="StrongPassword123",
        )

        self.shop = Shop.objects.create(
            owner=self.user,
            name="Elias Electronics",
        )

    def test_shop_list_requires_login(self):
        response = self.client.get(
            reverse("shops:shop_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_shop_list_shows_owned_shops(self):
        self.client.login(
            username="elias",
            password="StrongPassword123",
        )

        response = self.client.get(
            reverse("shops:shop_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_cannot_access_another_users_shop(self):
        self.client.login(
            username="abebe",
            password="StrongPassword123",
        )

        response = self.client.get(
            reverse(
                "shops:shop_detail",
                kwargs={
                    "slug": self.shop.slug,
                }
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_shop_detail_owner_can_access_shop(self):
        self.client.login(
            username="elias",
            password="StrongPassword123",
        )

        response = self.client.get(
            reverse(
                "shops:shop_detail",
                kwargs={
                    "slug": self.shop.slug,
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

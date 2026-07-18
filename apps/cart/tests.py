


from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from apps.products.models import Category, Product

from .models import Cart, CartItem
from .services import CartService


User = get_user_model()


class CartModelTests(TestCase):
    """
    Tests for Cart and CartItem models.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123!",
        )

        self.category = Category.objects.create(
            name="Electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="Test laptop",
            price=Decimal("1000.00"),
            stock=10,
            is_available=True,
        )

        self.cart = Cart.objects.create(
            owner=self.user,
        )

    def test_cart_belongs_to_user(self):
        self.assertEqual(
            self.cart.owner,
            self.user,
        )

    def test_cart_string_representation(self):
        self.assertEqual(
            str(self.cart),
            "elias's Cart",
        )

    def test_cart_item_string_representation(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(
            str(cart_item),
            "Laptop x 2",
        )

    def test_cart_item_subtotal(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(
            cart_item.subtotal,
            Decimal("2000.00"),
        )

    def test_cart_total_items(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(
            self.cart.total_items,
            2,
        )

    def test_cart_total_price(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(
            self.cart.total_price,
            Decimal("2000.00"),
        )

    def test_one_user_can_have_only_one_cart(self):
        with self.assertRaises(Exception):
            Cart.objects.create(
                owner=self.user,
            )

    def test_same_product_cannot_be_added_twice_as_cart_items(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
        )

        with self.assertRaises(Exception):
            CartItem.objects.create(
                cart=self.cart,
                product=self.product,
                quantity=1,
            )


class CartServiceTests(TestCase):
    """
    Tests for CartService business logic.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123!",
        )

        self.category = Category.objects.create(
            name="Electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="Test laptop",
            price=Decimal("1000.00"),
            stock=10,
            is_available=True,
        )

        self.second_product = Product.objects.create(
            category=self.category,
            name="Mouse",
            description="Test mouse",
            price=Decimal("50.00"),
            stock=20,
            is_available=True,
        )

        self.cart = Cart.objects.create(
            owner=self.user,
        )

    def test_get_or_create_cart_creates_cart(self):
        self.cart.delete()

        cart = CartService.get_or_create_cart(
            user=self.user,
        )

        self.assertEqual(
            cart.owner,
            self.user,
        )

        self.assertEqual(
            Cart.objects.count(),
            1,
        )

    def test_get_or_create_cart_returns_existing_cart(self):
        cart = CartService.get_or_create_cart(
            user=self.user,
        )

        self.assertEqual(
            cart,
            self.cart,
        )

        self.assertEqual(
            Cart.objects.count(),
            1,
        )

    def test_add_product_to_cart(self):
        cart_item = CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(
            cart_item.quantity,
            2,
        )

        self.assertEqual(
            self.cart.items.count(),
            1,
        )

    def test_add_same_product_increases_quantity(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=3,
        )

        cart_item = CartItem.objects.get(
            cart=self.cart,
            product=self.product,
        )

        self.assertEqual(
            cart_item.quantity,
            5,
        )

        self.assertEqual(
            self.cart.items.count(),
            1,
        )

    def test_add_product_rejects_zero_quantity(self):
        with self.assertRaises(ValueError):
            CartService.add_product(
                cart=self.cart,
                product=self.product,
                quantity=0,
            )

    def test_add_product_rejects_negative_quantity(self):
        with self.assertRaises(ValueError):
            CartService.add_product(
                cart=self.cart,
                product=self.product,
                quantity=-1,
            )

    def test_update_quantity(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        cart_item = CartService.update_quantity(
            cart=self.cart,
            product=self.product,
            quantity=5,
        )

        self.assertEqual(
            cart_item.quantity,
            5,
        )

    def test_update_quantity_rejects_zero(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        with self.assertRaises(ValueError):
            CartService.update_quantity(
                cart=self.cart,
                product=self.product,
                quantity=0,
            )

    def test_remove_product(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        result = CartService.remove_product(
            cart=self.cart,
            product=self.product,
        )

        self.assertTrue(result)

        self.assertFalse(
            CartItem.objects.filter(
                cart=self.cart,
                product=self.product,
            ).exists()
        )

    def test_remove_nonexistent_product_returns_false(self):
        result = CartService.remove_product(
            cart=self.cart,
            product=self.product,
        )

        self.assertFalse(result)

    def test_clear_cart(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        CartService.add_product(
            cart=self.cart,
            product=self.second_product,
            quantity=1,
        )

        CartService.clear_cart(
            cart=self.cart,
        )

        self.assertEqual(
            self.cart.items.count(),
            0,
        )

    def test_get_cart_items(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=1,
        )

        items = CartService.get_cart_items(
            cart=self.cart,
        )

        self.assertEqual(
            items.count(),
            1,
        )

        self.assertEqual(
            items.first().product,
            self.product,
        )

    def test_get_cart_summary(self):
        CartService.add_product(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        summary = CartService.get_cart_summary(
            cart=self.cart,
        )

        self.assertEqual(
            summary["cart"],
            self.cart,
        )

        self.assertEqual(
            summary["total_items"],
            2,
        )

        self.assertEqual(
            summary["total_price"],
            Decimal("2000.00"),
        )


class CartViewTests(TestCase):
    """
    Tests for Cart views.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="StrongPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="abebe",
            email="abebe@example.com",
            password="StrongPassword123!",
        )

        self.category = Category.objects.create(
            name="Electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="Test laptop",
            price=Decimal("1000.00"),
            stock=10,
            is_available=True,
        )

        self.client.login(
            username="elias",
            password="StrongPassword123!",
        )

    @patch(
        "apps.cart.views.render",
        return_value=HttpResponse(
            "Cart detail"
        ),
    )
    def test_cart_detail_creates_cart_for_user(
        self,
        mock_render,
    ):
        response = self.client.get(
            reverse("cart:cart_detail")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            Cart.objects.filter(
                owner=self.user,
            ).exists()
        )

        mock_render.assert_called_once()

    def test_add_product_to_cart(self):
        response = self.client.post(
            reverse(
                "cart:add_to_cart",
                kwargs={
                    "product_id": self.product.id,
                },
            ),
            {
                "quantity": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        cart = Cart.objects.get(
            owner=self.user,
        )

        cart_item = CartItem.objects.get(
            cart=cart,
            product=self.product,
        )

        self.assertEqual(
            cart_item.quantity,
            2,
        )

    def test_unavailable_product_cannot_be_added(self):
        self.product.is_available = False

        self.product.save(
            update_fields=[
                "is_available",
            ]
        )

        response = self.client.post(
            reverse(
                "cart:add_to_cart",
                kwargs={
                    "product_id": self.product.id,
                },
            ),
            {
                "quantity": 1,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_update_cart_item(self):
        cart = CartService.get_or_create_cart(
            user=self.user,
        )

        CartService.add_product(
            cart=cart,
            product=self.product,
            quantity=1,
        )

        response = self.client.post(
            reverse(
                "cart:update_cart_item",
                kwargs={
                    "product_id": self.product.id,
                },
            ),
            {
                "quantity": 5,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        cart_item = CartItem.objects.get(
            cart=cart,
            product=self.product,
        )

        self.assertEqual(
            cart_item.quantity,
            5,
        )

    def test_remove_product_from_cart(self):
        cart = CartService.get_or_create_cart(
            user=self.user,
        )

        CartService.add_product(
            cart=cart,
            product=self.product,
            quantity=1,
        )

        response = self.client.post(
            reverse(
                "cart:remove_from_cart",
                kwargs={
                    "product_id": self.product.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            CartItem.objects.filter(
                cart=cart,
                product=self.product,
            ).exists()
        )

    def test_clear_cart(self):
        cart = CartService.get_or_create_cart(
            user=self.user,
        )

        CartService.add_product(
            cart=cart,
            product=self.product,
            quantity=1,
        )

        response = self.client.post(
            reverse("cart:clear_cart")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            cart.items.count(),
            0,
        )

    def test_user_can_only_access_own_cart(self):
        elias_cart = CartService.get_or_create_cart(
            user=self.user,
        )

        abebe_cart = CartService.get_or_create_cart(
            user=self.other_user,
        )

        CartService.add_product(
            cart=elias_cart,
            product=self.product,
            quantity=2,
        )

        self.assertNotEqual(
            elias_cart,
            abebe_cart,
        )

        self.assertEqual(
            elias_cart.owner,
            self.user,
        )

        self.assertEqual(
            abebe_cart.owner,
            self.other_user,
        )

        self.assertEqual(
            elias_cart.total_items,
            2,
        )

        self.assertEqual(
            abebe_cart.total_items,
            0,
        )

    def test_anonymous_user_cannot_access_cart(self):
        self.client.logout()

        response = self.client.get(
            reverse("cart:cart_detail")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_anonymous_user_cannot_add_product(self):
        self.client.logout()

        response = self.client.post(
            reverse(
                "cart:add_to_cart",
                kwargs={
                    "product_id": self.product.id,
                },
            ),
            {
                "quantity": 1,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )



from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.cart.models import Cart, CartItem
from apps.products.models import Category, Product

from .forms import CheckoutForm
from .models import Order, OrderItem
from .services import OrderService
from .utils import generate_order_number


User = get_user_model()


class OrderTestMixin:
    """
    Shared test setup for Orders tests.
    """

    def create_user(
        self,
        username="elias",
        email="elias@example.com",
        password="StrongPassword123!",
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

    def create_category(self):
        return Category.objects.create(
            name="Electronics",
        )

    def create_product(
        self,
        category,
        name="Wireless Headphones",
        price=Decimal("500.00"),
    ):
        return Product.objects.create(
            category=category,
            name=name,
            description="A test product",
            price=price,
            stock=10,
            is_available=True,
        )

    def create_cart(self, user):
        return Cart.objects.create(
            owner=user,
        )


class GenerateOrderNumberTests(TestCase):
    """
    Tests for order number generation.
    """

    def test_order_number_has_correct_prefix(self):
        order_number = generate_order_number()

        self.assertTrue(
            order_number.startswith("ORD-")
        )

    def test_order_number_has_expected_structure(self):
        order_number = generate_order_number()

        parts = order_number.split("-")

        self.assertEqual(
            len(parts),
            3,
        )

        self.assertEqual(
            parts[0],
            "ORD",
        )

        self.assertEqual(
            len(parts[1]),
            14,
        )

        self.assertEqual(
            len(parts[2]),
            4,
        )

    def test_order_numbers_are_different(self):
        first_order_number = generate_order_number()
        second_order_number = generate_order_number()

        self.assertNotEqual(
            first_order_number,
            second_order_number,
        )


class OrderModelTests(OrderTestMixin, TestCase):
    """
    Tests for Order and OrderItem models.
    """

    def setUp(self):
        self.user = self.create_user()

        self.category = self.create_category()

        self.product = self.create_product(
            category=self.category,
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number=generate_order_number(),
            total_amount=Decimal("500.00"),
            shipping_address="Bole, Addis Ababa",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

    def test_order_string_representation(self):
        self.assertEqual(
            str(self.order),
            self.order.order_number,
        )

    def test_order_default_status_is_pending(self):
        self.assertEqual(
            self.order.status,
            Order.Status.PENDING,
        )

    def test_order_item_string_representation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            unit_price=self.product.price,
            quantity=1,
            subtotal=self.product.price,
        )

        self.assertEqual(
            str(order_item),
            "Wireless Headphones × 1",
        )


class CheckoutFormTests(TestCase):
    """
    Tests for CheckoutForm validation.
    """

    def valid_form_data(self):
        return {
            "shipping_address": (
                "Bole, Addis Ababa, near Edna Mall"
            ),
            "shipping_city": "Addis Ababa",
            "shipping_phone": "0912345678",
        }

    def test_valid_checkout_form(self):
        form = CheckoutForm(
            data=self.valid_form_data(),
        )

        self.assertTrue(
            form.is_valid(),
        )

    def test_short_shipping_address_is_invalid(self):
        data = self.valid_form_data()

        data["shipping_address"] = "Short"

        form = CheckoutForm(data=data)

        self.assertFalse(
            form.is_valid(),
        )

        self.assertIn(
            "shipping_address",
            form.errors,
        )

    def test_short_city_is_invalid(self):
        data = self.valid_form_data()

        data["shipping_city"] = "A"

        form = CheckoutForm(data=data)

        self.assertFalse(
            form.is_valid(),
        )

        self.assertIn(
            "shipping_city",
            form.errors,
        )

    def test_short_phone_is_invalid(self):
        data = self.valid_form_data()

        data["shipping_phone"] = "123"

        form = CheckoutForm(data=data)

        self.assertFalse(
            form.is_valid(),
        )

        self.assertIn(
            "shipping_phone",
            form.errors,
        )

    def test_shipping_address_is_stripped(self):
        data = self.valid_form_data()

        data["shipping_address"] = (
            "   Bole, Addis Ababa, near Edna Mall   "
        )

        form = CheckoutForm(data=data)

        self.assertTrue(
            form.is_valid(),
        )

        self.assertEqual(
            form.cleaned_data["shipping_address"],
            "Bole, Addis Ababa, near Edna Mall",
        )


class OrderServiceTests(OrderTestMixin, TestCase):
    """
    Tests for OrderService business logic.
    """

    def setUp(self):
        self.user = self.create_user()

        self.category = self.create_category()

        self.product = self.create_product(
            category=self.category,
        )

        self.cart = self.create_cart(
            user=self.user,
        )

    def test_calculate_order_total(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        total = OrderService.calculate_order_total(
            cart=self.cart,
        )

        self.assertEqual(
            total,
            Decimal("1000.00"),
        )

    def test_create_order_from_cart(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        order = OrderService.create_order_from_cart(
            cart=self.cart,
            shipping_address="Bole, Addis Ababa",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

        self.assertEqual(
            order.user,
            self.user,
        )

        self.assertEqual(
            order.total_amount,
            Decimal("1000.00"),
        )

        self.assertEqual(
            order.items.count(),
            1,
        )

    def test_order_item_stores_product_snapshot(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
        )

        order = OrderService.create_order_from_cart(
            cart=self.cart,
            shipping_address="Bole, Addis Ababa",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

        order_item = order.items.first()

        self.assertEqual(
            order_item.product_name,
            self.product.name,
        )

        self.assertEqual(
            order_item.unit_price,
            self.product.price,
        )

    def test_get_user_orders_returns_only_user_orders(self):
        other_user = self.create_user(
            username="other",
            email="other@example.com",
        )

        Order.objects.create(
            user=self.user,
            order_number=generate_order_number(),
            total_amount=Decimal("500.00"),
            shipping_address="Bole",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

        Order.objects.create(
            user=other_user,
            order_number=generate_order_number(),
            total_amount=Decimal("500.00"),
            shipping_address="Bole",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

        orders = OrderService.get_user_orders(
            user=self.user,
        )

        self.assertEqual(
            orders.count(),
            1,
        )

        self.assertEqual(
            orders.first().user,
            self.user,
        )

    def test_get_order_returns_user_order(self):
        order = Order.objects.create(
            user=self.user,
            order_number=generate_order_number(),
            total_amount=Decimal("500.00"),
            shipping_address="Bole",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

        result = OrderService.get_order(
            order_number=order.order_number,
            user=self.user,
        )

        self.assertEqual(
            result,
            order,
        )


class OrderViewTests(OrderTestMixin, TestCase):
    """
    Tests for Orders views.
    """

    def setUp(self):
        self.user = self.create_user()

        self.cart = self.create_cart(
            user=self.user,
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number=generate_order_number(),
            total_amount=Decimal("500.00"),
            shipping_address="Bole, Addis Ababa",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

    def test_order_list_requires_login(self):
        response = self.client.get(
            reverse("orders:order_list"),
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_order_detail_requires_login(self):
        response = self.client.get(
            reverse(
                "orders:order_detail",
                kwargs={
                    "order_number": self.order.order_number,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_checkout_requires_login(self):
        response = self.client.get(
            reverse("orders:checkout"),
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_user_can_access_order_list(self):
        self.client.force_login(
            self.user,
        )

        response = self.client.get(
            reverse("orders:order_list"),
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_can_access_own_order_detail(self):
        self.client.force_login(
            self.user,
        )

        response = self.client.get(
            reverse(
                "orders:order_detail",
                kwargs={
                    "order_number": self.order.order_number,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_cannot_access_another_users_order(self):
        other_user = self.create_user(
            username="other",
            email="other@example.com",
        )

        other_order = Order.objects.create(
            user=other_user,
            order_number=generate_order_number(),
            total_amount=Decimal("500.00"),
            shipping_address="Bole",
            shipping_city="Addis Ababa",
            shipping_phone="0912345678",
        )

        self.client.force_login(
            self.user,
        )

        response = self.client.get(
            reverse(
                "orders:order_detail",
                kwargs={
                    "order_number": (
                        other_order.order_number
                    ),
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            404,
        )



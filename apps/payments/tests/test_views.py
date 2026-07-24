


from decimal import Decimal
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.models import Payment


User = get_user_model()


class PaymentViewTests(TestCase):
    """
    Tests for payment views.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="password123",
        )

        self.client.login(
            username="elias",
            password="password123",
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD-10001",
            total_amount=Decimal("250.00"),
            shipping_address="Addis Ababa",
            shipping_city="Addis Ababa",
            shipping_phone="0911000000",
        )


    def test_payment_list_requires_login(self):

        self.client.logout()

        response = self.client.get(
            reverse("payments:list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )


    def test_payment_list_authenticated_user(self):

        response = self.client.get(
            reverse("payments:list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_create_payment_page_loads(self):

        response = self.client.get(
            reverse(
                "payments:create",
                kwargs={
                    "order_id": self.order.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_create_payment_success(self):

        response = self.client.post(
            reverse(
                "payments:create",
                kwargs={
                    "order_id": self.order.id
                },
            ),
            data={
                "gateway": "chapa",
            },
        )


        self.assertIn(
            response.status_code,
            [
                200,
                302,
            ],
        )


        self.assertTrue(
            Payment.objects.filter(
                order=self.order
            ).exists()
        )


    @patch(
        "apps.payments.services.PaymentService.initialize_payment"
    )
    def test_checkout_initializes_gateway(
        self,
        mock_initialize,
    ):

        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway="chapa",
            amount=Decimal("250.00"),
            currency="ETB",
        )


        mock_initialize.return_value = {
            "checkout_url":
                "https://gateway.example.com/pay"
        }


        response = self.client.get(
            reverse(
                "payments:checkout",
                kwargs={
                    "payment_id": payment.id
                },
            )
        )


        self.assertIn(
            response.status_code,
            [
                200,
                302,
            ],
        )


        mock_initialize.assert_called_once()


    def test_user_cannot_access_other_users_payment(self):

        another_user = User.objects.create_user(
            username="other",
            password="password123",
        )


        another_order = Order.objects.create(
            user=another_user,
            order_number="ORD-20002",
            total_amount=Decimal("100.00"),
            shipping_address="Dire Dawa",
            shipping_city="Dire Dawa",
            shipping_phone="0900000000",
        )


        payment = Payment.objects.create(
            order=another_order,
            user=another_user,
            gateway="chapa",
            amount=Decimal("100.00"),
            currency="ETB",
        )


        response = self.client.get(
            reverse(
                "payments:checkout",
                kwargs={
                    "payment_id": payment.id
                },
            )
        )


        self.assertIn(
            response.status_code,
            [
                403,
                404,
            ],
        )


    def test_payment_success_page(self):

        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway="stripe",
            amount=Decimal("250.00"),
            currency="ETB",
            status=Payment.Status.COMPLETED,
        )


        response = self.client.get(
            reverse(
                "payments:success",
                kwargs={
                    "payment_id": payment.id
                },
            )
        )


        self.assertEqual(
            response.status_code,
            200,
        )




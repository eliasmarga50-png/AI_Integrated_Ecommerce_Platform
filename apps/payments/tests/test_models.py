


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.models import Payment

User = get_user_model()


class PaymentModelTests(TestCase):
    """
    Tests for the Payment model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
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

        self.payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway=Payment.Gateway.CHAPA,
            amount=Decimal("250.00"),
            currency="ETB",
        )

    def test_create_payment(self):
        """
        Payment object should be created successfully.
        """
        self.assertIsInstance(self.payment, Payment)

    def test_default_status(self):
        """
        Newly created payment should be pending.
        """
        self.assertEqual(
            self.payment.status,
            Payment.Status.PENDING,
        )

    def test_amount_is_saved(self):
        """
        Amount should be stored correctly.
        """
        self.assertEqual(
            self.payment.amount,
            Decimal("250.00"),
        )

    def test_currency_is_saved(self):
        """
        Currency should be stored correctly.
        """
        self.assertEqual(
            self.payment.currency,
            "ETB",
        )

    def test_gateway_is_saved(self):
        """
        Gateway should be stored correctly.
        """
        self.assertEqual(
            self.payment.gateway,
            Payment.Gateway.CHAPA,
        )

    def test_order_relationship(self):
        """
        Payment should belong to the correct order.
        """
        self.assertEqual(
            self.payment.order,
            self.order,
        )

    def test_user_relationship(self):
        """
        Payment should belong to the correct user.
        """
        self.assertEqual(
            self.payment.user,
            self.user,
        )

    def test_transaction_reference_exists(self):
        """
        Transaction reference should be generated.
        """
        self.assertTrue(
            self.payment.transaction_reference
        )

    def test_string_representation(self):
        expected = (
            f"Payment {self.payment.id} "
            f"- {self.payment.amount} "
            f"{self.payment.currency} "
            f"- {self.payment.get_status_display()}"
        )
        
        self.assertEqual(
            str(self.payment),
            expected,
        )

    def test_created_timestamp_exists(self):
        """
        Payment should have a creation timestamp.
        """
        self.assertIsNotNone(
            self.payment.created_at
        )
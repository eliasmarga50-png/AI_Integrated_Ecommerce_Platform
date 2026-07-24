



from decimal import Decimal
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.services import PaymentService
from apps.payments.exceptions import (
    AmountMismatchError,
    CurrencyMismatchError,
    DuplicatePaymentError,
    InvalidPaymentStateError,
    InvalidTransactionError,
)


User = get_user_model()


class PaymentServiceTests(TestCase):

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
            gateway="chapa",
            amount=Decimal("250.00"),
            currency="ETB",
        )


    def test_get_gateway_returns_correct_gateway(self):

        gateway = PaymentService.get_gateway(
            "chapa"
        )

        self.assertIsNotNone(gateway)


    def test_get_gateway_invalid_provider(self):

        with self.assertRaises(ValueError):

            PaymentService.get_gateway(
                "bitcoin"
            )


    @patch(
        "apps.payments.services.Payment.objects.create"
    )
    def test_create_payment(
        self,
        mock_create,
    ):

        mock_create.return_value = self.payment

        payment = PaymentService.create_payment(
            order=self.order,
            user=self.user,
            gateway="chapa",
        )

        self.assertEqual(
            payment,
            self.payment,
        )


    def test_duplicate_payment_not_allowed(self):

        with self.assertRaises(
            DuplicatePaymentError
        ):

            PaymentService.create_payment(
                order=self.order,
                user=self.user,
                gateway="chapa",
            )


    @patch(
        "apps.payments.services.PaymentService.get_gateway"
    )
    def test_initialize_payment(
        self,
        mock_gateway,
    ):

        gateway = Mock()

        gateway.initialize_payment.return_value = {
            "checkout_url": "https://example.com/pay"
        }

        mock_gateway.return_value = gateway


        result = PaymentService.initialize_payment(
            self.payment
        )


        self.assertIn(
            "checkout_url",
            result,
        )


    @patch(
        "apps.payments.services.PaymentService.get_gateway"
    )
    def test_verify_payment_success(
        self,
        mock_gateway,
    ):

        gateway = Mock()

        gateway.verify_payment.return_value = {
            "verified": True,
            "amount": "250.00",
            "currency": "ETB",
            "gateway_reference": "TXN123",
        }

        mock_gateway.return_value = gateway


        result = PaymentService.verify_payment(
            self.payment
        )


        self.assertTrue(
            result["verified"]
        )


        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.COMPLETED,
        )


    @patch(
        "apps.payments.services.PaymentService.get_gateway"
    )
    def test_verify_payment_wrong_amount(
        self,
        mock_gateway,
    ):

        gateway = Mock()

        gateway.verify_payment.return_value = {
            "verified": True,
            "amount": "100.00",
            "currency": "ETB",
        }

        mock_gateway.return_value = gateway


        with self.assertRaises(
            AmountMismatchError
        ):

            PaymentService.verify_payment(
                self.payment
            )


    @patch(
        "apps.payments.services.PaymentService.get_gateway"
    )
    def test_verify_payment_wrong_currency(
        self,
        mock_gateway,
    ):

        gateway = Mock()

        gateway.verify_payment.return_value = {
            "verified": True,
            "amount": "250.00",
            "currency": "USD",
        }

        mock_gateway.return_value = gateway


        with self.assertRaises(
            CurrencyMismatchError
        ):

            PaymentService.verify_payment(
                self.payment
            )


    @patch(
        "apps.payments.services.PaymentService.get_gateway"
    )
    def test_gateway_verification_failed(
        self,
        mock_gateway,
    ):

        gateway = Mock()

        gateway.verify_payment.return_value = {
            "verified": False,
        }

        mock_gateway.return_value = gateway


        with self.assertRaises(
            InvalidTransactionError
        ):

            PaymentService.verify_payment(
                self.payment
            )


    def test_mark_completed(self):

        PaymentService.mark_completed(
            self.payment,
            gateway_reference="TXN001",
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.COMPLETED,
        )


    def test_cannot_complete_twice(self):

        self.payment.status = (
            Payment.Status.COMPLETED
        )

        self.payment.save()


        with self.assertRaises(
            InvalidPaymentStateError
        ):

            PaymentService.mark_completed(
                self.payment
            )


    @patch(
        "apps.payments.services.PaymentService.get_gateway"
    )
    def test_refund_payment(
        self,
        mock_gateway,
    ):

        gateway = Mock()

        gateway.refund_payment.return_value = {
            "success": True
        }

        mock_gateway.return_value = gateway


        result = PaymentService.refund_payment(
            self.payment
        )


        self.assertTrue(
            result["success"]
        )



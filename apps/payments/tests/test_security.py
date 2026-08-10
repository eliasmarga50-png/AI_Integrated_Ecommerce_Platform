


from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.exceptions import (
    AmountMismatchError,
    CurrencyMismatchError,
    DuplicatePaymentError,
    InvalidPaymentStateError,
    InvalidTransactionError,
    ReplayAttackError,
    SignatureVerificationError,
)
from apps.payments.models import Payment
from apps.payments.services import PaymentService
from apps.payments.webhooks import PaymentWebhookHandler


User = get_user_model()


class PaymentSecurityTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="password123",
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD-SEC-001",
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

        self.handler = PaymentWebhookHandler(
            gateway="chapa",
            gateway_secret="secret123",
        )

    @patch(
        "apps.payments.webhooks.verify_hmac_signature",
        return_value=False,
    )
    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=True,
    )
    def test_invalid_signature_rejected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id": self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "ETB",
        }

        with self.assertRaises(
            SignatureVerificationError
        ):
            self.handler.process_webhook(
                payload=payload,
                signature="bad-signature",
                timestamp="123456",
            )

    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=False,
    )
    def test_expired_timestamp_rejected(
        self,
        mock_timestamp,
    ):

        with self.assertRaises(
            ReplayAttackError
        ):
            self.handler.process_webhook(
                payload={},
                signature="sig",
                timestamp="old",
            )

    @patch(
        "apps.payments.webhooks.verify_hmac_signature",
        return_value=True,
    )
    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=True,
    )
    def test_amount_tampering_detected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id": self.payment.transaction_reference,
            "amount": "1.00",
            "currency": "ETB",
        }

        with self.assertRaises(
            AmountMismatchError
        ):
            self.handler.process_webhook(
                payload=payload,
                signature="valid",
                timestamp="123",
            )

    @patch(
        "apps.payments.webhooks.verify_hmac_signature",
        return_value=True,
    )
    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=True,
    )
    def test_currency_tampering_detected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id": self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "USD",
        }

        with self.assertRaises(
            CurrencyMismatchError
        ):
            self.handler.process_webhook(
                payload=payload,
                signature="valid",
                timestamp="123",
            )

    @patch(
        "apps.payments.webhooks.verify_hmac_signature",
        return_value=True,
    )
    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=True,
    )
    def test_unknown_transaction_rejected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id": "INVALID",
            "amount": "250.00",
            "currency": "ETB",
        }

        with self.assertRaises(
            InvalidTransactionError
        ):
            self.handler.process_webhook(
                payload=payload,
                signature="valid",
                timestamp="123",
            )

    def test_duplicate_payment_creation_blocked(self):

        with self.assertRaises(
            DuplicatePaymentError
        ):
            PaymentService.create_payment(
                order=self.order,
                user=self.user,
                gateway="chapa",
            )

    def test_completed_payment_cannot_be_completed_again(self):

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

    def test_invalid_gateway_rejected(self):

        with self.assertRaises(
            ValueError
        ):
            PaymentService.get_gateway(
                "fake_gateway"
            )

    @patch(
        "apps.payments.webhooks.verify_hmac_signature",
        return_value=True,
    )
    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=True,
    )
    def test_replay_attack_blocked(
        self,
        mock_timestamp,
        mock_signature,
    ):

        self.payment.status = (
            Payment.Status.COMPLETED
        )
        self.payment.save()

        payload = {
            "transaction_id": self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "ETB",
        }

        with self.assertRaises(
            ReplayAttackError
        ):
            self.handler.process_webhook(
                payload=payload,
                signature="valid",
                timestamp="123",
            )




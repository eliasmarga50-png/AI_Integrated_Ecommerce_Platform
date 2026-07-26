


from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.webhooks import (
    PaymentWebhookHandler,
    payment_webhook_response,
)

from apps.payments.exceptions import (
    AmountMismatchError,
    CurrencyMismatchError,
    InvalidTransactionError,
    ReplayAttackError,
    SignatureVerificationError,
)


User = get_user_model()


class PaymentWebhookTests(TestCase):

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

        self.handler = PaymentWebhookHandler(
            gateway_secret="secret123"
        )


    @patch(
        "apps.payments.webhooks.verify_hmac_signature",
        return_value=True,
    )
    @patch(
        "apps.payments.webhooks.is_timestamp_valid",
        return_value=True,
    )
    @patch(
        "apps.payments.webhooks.PaymentService.mark_completed",
    )
    def test_valid_webhook_completes_payment(
        self,
        mock_complete,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id":
                self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "ETB",
        }


        self.handler.process_webhook(
            payload=payload,
            signature="valid-signature",
            timestamp="123456",
        )


        mock_complete.assert_called_once()


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
            "transaction_id":
                self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "ETB",
        }


        with self.assertRaises(
            SignatureVerificationError
        ):

            self.handler.process_webhook(
                payload=payload,
                signature="wrong",
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
                signature="signature",
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
    def test_missing_transaction_rejected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "amount": "250.00",
            "currency": "ETB",
        }


        with self.assertRaises(
            InvalidTransactionError
        ):

            self.handler.process_webhook(
                payload=payload,
                signature="signature",
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
            "transaction_id": "UNKNOWN",
            "amount": "250.00",
            "currency": "ETB",
        }


        with self.assertRaises(
            InvalidTransactionError
        ):

            self.handler.process_webhook(
                payload=payload,
                signature="signature",
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
    def test_wrong_amount_rejected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id":
                self.payment.transaction_reference,
            "amount": "100.00",
            "currency": "ETB",
        }


        with self.assertRaises(
            AmountMismatchError
        ):

            self.handler.process_webhook(
                payload=payload,
                signature="signature",
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
    def test_wrong_currency_rejected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        payload = {
            "transaction_id":
                self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "USD",
        }


        with self.assertRaises(
            CurrencyMismatchError
        ):

            self.handler.process_webhook(
                payload=payload,
                signature="signature",
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
    def test_completed_payment_replay_rejected(
        self,
        mock_timestamp,
        mock_signature,
    ):

        self.payment.status = (
            Payment.Status.COMPLETED
        )

        self.payment.save()


        payload = {
            "transaction_id":
                self.payment.transaction_reference,
            "amount": "250.00",
            "currency": "ETB",
        }


        with self.assertRaises(
            ReplayAttackError
        ):

            self.handler.process_webhook(
                payload=payload,
                signature="signature",
                timestamp="123",
            )


    @patch(
        "apps.payments.webhooks.PaymentWebhookHandler.process_webhook"
    )
    def test_webhook_response_success(
        self,
        mock_process,
    ):

        mock_process.return_value = self.payment

        factory = RequestFactory()

        request = factory.post(
            "/payments/webhook/",
            data="{}",
            content_type="application/json",
        )


        response = payment_webhook_response(
            self.handler,
            request,
        )


        self.assertEqual(
            response.status_code,
            200,
        )



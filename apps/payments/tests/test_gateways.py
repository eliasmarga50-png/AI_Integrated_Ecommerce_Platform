


from decimal import Decimal
from unittest.mock import Mock, patch

from django.test import TestCase

from apps.payments.gateways.chapa import ChapaGateway
from apps.payments.gateways.paypal import PayPalGateway
from apps.payments.gateways.stripe import StripeGateway
from apps.payments.gateways.telebirr import TelebirrGateway


class GatewayTests(TestCase):
    """
    Tests for supported payment gateways.

    External payment providers are mocked so that
    these tests never make real network requests.
    """

    def setUp(self):
        self.payment = Mock()

        self.payment.id = 1
        self.payment.amount = Decimal("250.00")
        self.payment.currency = "ETB"
        self.payment.transaction_reference = "PAY-123456"
        self.payment.gateway_reference = None

        self.payment.user = Mock()
        self.payment.user.id = 1
        self.payment.user.email = "elias@example.com"
        self.payment.user.first_name = "Elias"
        self.payment.user.last_name = "Marga"

        self.payment.order = Mock()
        self.payment.order.id = 1

    # =====================================================
    # CHAPA
    # =====================================================

    @patch.object(ChapaGateway, "request")
    def test_chapa_initialize_payment(
        self,
        mock_request,
    ):
        mock_request.return_value = {
            "success": True,
            "status_code": 200,
            "data": {
                "status": "success",
                "data": {
                    "checkout_url":
                        "https://checkout.chapa.co/test"
                },
            },
        }

        gateway = ChapaGateway()

        response = gateway.initialize_payment(
            self.payment
        )

        self.assertTrue(
            response["success"]
        )

        self.assertIn(
            "checkout_url",
            response["data"]["data"],
        )

        mock_request.assert_called_once()

    @patch.object(ChapaGateway, "request")
    def test_chapa_verify_payment(
        self,
        mock_request,
    ):
        mock_request.return_value = {
            "success": True,
            "status_code": 200,
            "data": {
                "status": "success",
            },
        }

        gateway = ChapaGateway()

        response = gateway.verify_payment(
            "PAY-123"
        )

        self.assertIsNotNone(response)

        mock_request.assert_called_once()

    def test_chapa_normalize_verification(self):
        gateway = ChapaGateway()

        raw = {
            "status": "success",
            "data": {
                "tx_ref": "PAY-123",
                "reference": "CHAPA-001",
                "amount": "250.00",
                "currency": "ETB",
                "status": "success",
            },
        }

        normalized = gateway.normalize_verification(
            raw
        )

        self.assertTrue(
            normalized["verified"]
        )

        self.assertEqual(
            normalized["amount"],
            "250.00",
        )

        self.assertEqual(
            normalized["currency"],
            "ETB",
        )

        self.assertEqual(
            normalized["transaction_reference"],
            "PAY-123",
        )

    # =====================================================
    # TELEBIRR
    # =====================================================

    @patch.object(
        TelebirrGateway,
        "sign_payload",
        return_value="TEST-SIGNATURE",
    )
    @patch.object(
        TelebirrGateway,
        "request",
    )
    def test_telebirr_initialize_payment(
        self,
        mock_request,
        mock_sign,
    ):
        mock_request.return_value = {
            "success": True,
            "status_code": 200,
            "data": {
                "code": "SUCCESS",
            },
        }

        gateway = TelebirrGateway()

        result = gateway.initialize_payment(
            self.payment
        )

        self.assertIsNotNone(result)

        self.assertTrue(
            result["success"]
        )

        mock_sign.assert_called_once()

        mock_request.assert_called_once()

    # =====================================================
    # STRIPE
    # =====================================================

    @patch(
        "apps.payments.gateways.stripe.stripe.PaymentIntent.create"
    )
    def test_stripe_initialize_payment(
        self,
        mock_create,
    ):
        mock_intent = Mock()

        mock_intent.id = "pi_test"
        mock_intent.client_secret = (
            "secret_test"
        )
        mock_intent.status = "requires_payment_method"

        mock_create.return_value = mock_intent

        gateway = StripeGateway()

        result = gateway.initialize_payment(
            self.payment
        )

        self.assertIsNotNone(result)

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["payment_intent_id"],
            "pi_test",
        )

        mock_create.assert_called_once()

        call_kwargs = (
            mock_create.call_args.kwargs
        )

        self.assertEqual(
            call_kwargs["amount"],
            25000,
        )

        self.assertEqual(
            call_kwargs["currency"],
            "etb",
        )

    # =====================================================
    # PAYPAL
    # =====================================================

    @patch(
        "apps.payments.gateways.paypal.PaypalServersdkClient"
    )
    def test_paypal_initialize_payment(
        self,
        mock_client_class,
    ):
        mock_client = Mock()

        mock_orders = Mock()

        mock_result = Mock()

        mock_result.body = {
            "id": "PAYPAL-001",
            "status": "CREATED",
            "links": [
                {
                    "rel": "approve",
                    "href":
                        "https://paypal.test/approve",
                }
            ],
        }

        mock_orders.create_order.return_value = (
            mock_result
        )

        mock_client.orders = mock_orders

        mock_client_class.return_value = (
            mock_client
        )

        gateway = PayPalGateway()

        result = gateway.initialize_payment(
            self.payment
        )

        self.assertIsNotNone(result)

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["order_id"],
            "PAYPAL-001",
        )

        self.assertEqual(
            result["status"],
            "CREATED",
        )

        self.assertEqual(
            result["approval_url"],
            "https://paypal.test/approve",
        )

        mock_orders.create_order.assert_called_once()

    # =====================================================
    # NETWORK ERROR
    # =====================================================

    @patch.object(
        ChapaGateway,
        "request",
    )
    def test_gateway_network_error(
        self,
        mock_request,
    ):
        mock_request.side_effect = Exception(
            "Network Error"
        )

        gateway = ChapaGateway()

        with self.assertRaises(Exception):
            gateway.initialize_payment(
                self.payment
            )



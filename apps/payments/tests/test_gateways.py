


from unittest.mock import Mock, patch

from django.test import TestCase

from apps.payments.gateways.chapa import ChapaGateway
from apps.payments.gateways.paypal import PayPalGateway
from apps.payments.gateways.stripe import StripeGateway
from apps.payments.gateways.telebirr import TelebirrGateway


class GatewayTests(TestCase):
    """
    Tests for supported payment gateways.
    """

    def setUp(self):
        self.payment = Mock()
        self.payment.amount = "250.00"
        self.payment.currency = "ETB"
        self.payment.transaction_reference = "PAY-123456"
        self.payment.gateway_reference = None

    # -------------------------
    # Chapa
    # -------------------------

    @patch("requests.post")
    def test_chapa_initialize_payment(self, mock_post):

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "checkout_url": "https://checkout.chapa.co/test"
            },
        }

        mock_post.return_value = mock_response

        gateway = ChapaGateway()

        response = gateway.initialize_payment(
            self.payment
        )

        self.assertIn(
            "checkout_url",
            response,
        )

    @patch("requests.get")
    def test_chapa_verify_payment(self, mock_get):

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "status": "success"
        }

        mock_get.return_value = mock_response

        gateway = ChapaGateway()

        response = gateway.verify_payment(
            "PAY-123"
        )

        self.assertIsNotNone(response)

    def test_chapa_normalize_verification(self):

        gateway = ChapaGateway()

        raw = {
            "status": "success",
            "data": {
                "tx_ref": "PAY-123",
                "reference": "CHAPA-001",
                "amount": "250.00",
                "currency": "ETB",
            },
        }

        normalized = gateway.normalize_verification(raw)

        self.assertTrue(normalized["verified"])
        self.assertEqual(
            normalized["amount"],
            "250.00",
        )

    # -------------------------
    # Telebirr
    # -------------------------

    @patch("requests.post")
    def test_telebirr_initialize_payment(
        self,
        mock_post,
    ):

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "code": "SUCCESS"
        }

        mock_post.return_value = mock_response

        gateway = TelebirrGateway()

        result = gateway.initialize_payment(
            self.payment
        )

        self.assertIsNotNone(result)

    # -------------------------
    # Stripe
    # -------------------------

    @patch("requests.post")
    def test_stripe_initialize_payment(
        self,
        mock_post,
    ):

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "id": "pi_test"
        }

        mock_post.return_value = mock_response

        gateway = StripeGateway()

        result = gateway.initialize_payment(
            self.payment
        )

        self.assertIsNotNone(result)

    # -------------------------
    # PayPal
    # -------------------------

    @patch("requests.post")
    def test_paypal_initialize_payment(
        self,
        mock_post,
    ):

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "id": "PAYPAL-001"
        }

        mock_post.return_value = mock_response

        gateway = PayPalGateway()

        result = gateway.initialize_payment(
            self.payment
        )

        self.assertIsNotNone(result)

    @patch("requests.post")
    def test_gateway_network_error(
        self,
        mock_post,
    ):

        mock_post.side_effect = Exception(
            "Network Error"
        )

        gateway = ChapaGateway()

        with self.assertRaises(Exception):
            gateway.initialize_payment(
                self.payment
            )




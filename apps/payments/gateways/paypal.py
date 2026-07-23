


from django.conf import settings

from paypalserversdk.http.auth.o_auth_2 import ClientCredentialsAuthCredentials
from paypalserversdk.paypal_serversdk_client import PaypalServersdkClient

from .base import BasePaymentGateway


class PayPalGateway(BasePaymentGateway):
    """
    PayPal Orders API implementation.
    """

    def __init__(self):
        super().__init__()

        self.client = PaypalServersdkClient(
            client_credentials_auth_credentials=
            ClientCredentialsAuthCredentials(
                o_auth_client_id=settings.PAYPAL_CLIENT_ID,
                o_auth_client_secret=settings.PAYPAL_CLIENT_SECRET,
            ),
            environment=settings.PAYPAL_ENVIRONMENT,
        )

        self.orders = self.client.orders

    def initialize_payment(self, payment):
        """
        Create a PayPal order.
        """

        body = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": payment.transaction_reference,
                    "amount": {
                        "currency_code": payment.currency,
                        "value": str(payment.amount),
                    },
                    "description": (
                        f"AI_Ecommerce Order #{payment.order.id}"
                    ),
                }
            ],
            "application_context": {
                "return_url": settings.PAYPAL_RETURN_URL,
                "cancel_url": settings.PAYPAL_CANCEL_URL,
            },
        }

        result = self.orders.create_order(
            {
                "body": body,
                "prefer": "return=representation",
            }
        )

        order = result.body

        approval_url = None

        for link in order.get("links", []):

            if link.get("rel") == "approve":
                approval_url = link.get("href")
                break

        return {
            "success": True,
            "order_id": order["id"],
            "status": order["status"],
            "approval_url": approval_url,
            "raw": order,
        }

    def verify_payment(
        self,
        order_id,
    ):
        """
        Retrieve PayPal order details.
        """

        result = self.orders.get_order(
            {
                "id": order_id,
            }
        )

        return self.normalize_verification(
            result.body
        )

    def capture_payment(
        self,
        order_id,
    ):
        """
        Capture an approved order.
        """

        result = self.orders.capture_order(
            {
                "id": order_id,
            }
        )

        return self.normalize_verification(
            result.body
        )

    def refund_payment(
        self,
        payment,
    ):
        """
        Refund implementation can be added later.
        """

        raise NotImplementedError(
            "PayPal refund integration is not implemented."
        )

    def normalize_verification(
        self,
        order,
    ):
        """
        Convert PayPal responses into
        AI_Ecommerce's standard format.
        """

        purchase_unit = order["purchase_units"][0]

        amount = purchase_unit["amount"]

        return {
            "verified": (
                order["status"] == "COMPLETED"
            ),
            "transaction_reference": (
                purchase_unit.get("reference_id")
            ),
            "gateway_reference": order["id"],
            "amount": amount["value"],
            "currency": amount["currency_code"],
            "payment_method": "paypal",
            "status": order["status"],
            "raw": order,
        }
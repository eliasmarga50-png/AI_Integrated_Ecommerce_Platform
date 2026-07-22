


from django.conf import settings

from .base import BasePaymentGateway


class ChapaGateway(BasePaymentGateway):
    """
    Chapa payment gateway implementation.
    """

    base_url = getattr(
        settings,
        "CHAPA_BASE_URL",
        "https://api.chapa.co",
    )

    api_key = getattr(
        settings,
        "CHAPA_SECRET_KEY",
        None,
    )

    INITIALIZE_ENDPOINT = "/v1/transaction/initialize"

    VERIFY_ENDPOINT = "/v1/transaction/verify/{tx_ref}"

    def initialize_payment(self, payment):
        """
        Initialize a Chapa checkout transaction.
        """

        payload = {
            "amount": str(payment.amount),
            "currency": payment.currency,
            "email": payment.user.email,
            "first_name": payment.user.first_name,
            "last_name": payment.user.last_name,
            "tx_ref": payment.transaction_reference,
            "callback_url": settings.CHAPA_CALLBACK_URL,
            "return_url": settings.CHAPA_RETURN_URL,
            "customization": {
                "title": "AI_Ecommerce",
                "description": (
                    f"Payment for Order #{payment.order.id}"
                ),
            },
        }

        return self.request(
            method="POST",
            endpoint=self.INITIALIZE_ENDPOINT,
            data=payload,
        )

    def verify_payment(
        self,
        transaction_reference,
    ):
        """
        Verify a transaction with Chapa.
        """

        endpoint = self.VERIFY_ENDPOINT.format(
            tx_ref=transaction_reference,
        )

        return self.request(
            method="GET",
            endpoint=endpoint,
        )

    def refund_payment(
        self,
        payment,
    ):
        """
        Placeholder.

        Refund support can be added when the
        application introduces refund workflows.
        """

        raise NotImplementedError(
            "Refund integration is not implemented."
        )

    def normalize_verification(
        self,
        response,
    ):
        """
        Convert Chapa verification response
        into a provider-independent structure.
        """

        if not response["success"]:
            return response

        data = response["data"]

        payment_data = data.get(
            "data",
            {},
        )

        return {
            "verified": (
                payment_data.get("status")
                == "success"
            ),
            "transaction_reference": payment_data.get(
                "tx_ref"
            ),
            "gateway_reference": payment_data.get(
                "reference"
            ),
            "amount": payment_data.get(
                "amount"
            ),
            "currency": payment_data.get(
                "currency"
            ),
            "payment_method": payment_data.get(
                "method"
            ),
            "raw": data,
        }






from django.conf import settings

from .base import BasePaymentGateway


class TelebirrGateway(BasePaymentGateway):
    """
    Telebirr payment gateway.

    This implementation provides the production architecture.
    Merchant-specific endpoints, signing logic, and certificates
    should be completed using the official Telebirr merchant
    documentation issued to your organization.
    """

    base_url = getattr(
        settings,
        "TELEBIRR_BASE_URL",
        None,
    )

    api_key = getattr(
        settings,
        "TELEBIRR_APP_KEY",
        None,
    )

    merchant_id = getattr(
        settings,
        "TELEBIRR_MERCHANT_ID",
        None,
    )

    app_id = getattr(
        settings,
        "TELEBIRR_APP_ID",
        None,
    )

    private_key = getattr(
        settings,
        "TELEBIRR_PRIVATE_KEY",
        None,
    )

    public_key = getattr(
        settings,
        "TELEBIRR_PUBLIC_KEY",
        None,
    )

    INITIALIZE_ENDPOINT = "/payment/v1/initialize"

    VERIFY_ENDPOINT = "/payment/v1/query"

    REFUND_ENDPOINT = "/payment/v1/refund"

    def get_headers(self):
        """
        Telebirr-specific headers.

        Update these according to the official merchant
        documentation.
        """

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def build_payload(self, payment):
        """
        Build a payment payload.

        The exact field names depend on the
        Telebirr merchant specification.
        """

        return {
            "merchantId": self.merchant_id,
            "appId": self.app_id,
            "merchantOrderId": str(payment.order.id),
            "transactionReference": payment.transaction_reference,
            "amount": str(payment.amount),
            "currency": payment.currency,
            "notifyUrl": settings.TELEBIRR_CALLBACK_URL,
            "returnUrl": settings.TELEBIRR_RETURN_URL,
        }

    def sign_payload(self, payload):
        """
        Sign the request.

        Replace this implementation with the signing
        algorithm required by Telebirr.
        """

        raise NotImplementedError(
            "Implement Telebirr request signing."
        )

    def initialize_payment(self, payment):
        payload = self.build_payload(payment)

        payload["signature"] = self.sign_payload(
            payload
        )

        return self.request(
            method="POST",
            endpoint=self.INITIALIZE_ENDPOINT,
            data=payload,
        )

    def verify_payment(
        self,
        transaction_reference,
    ):
        payload = {
            "transactionReference":
                transaction_reference,
        }

        payload["signature"] = self.sign_payload(
            payload
        )

        return self.request(
            method="POST",
            endpoint=self.VERIFY_ENDPOINT,
            data=payload,
        )

    def refund_payment(
        self,
        payment,
    ):
        payload = {
            "transactionReference":
                payment.transaction_reference,
        }

        payload["signature"] = self.sign_payload(
            payload
        )

        return self.request(
            method="POST",
            endpoint=self.REFUND_ENDPOINT,
            data=payload,
        )

    def normalize_verification(
        self,
        response,
    ):
        """
        Convert Telebirr's response into the
        common application format.
        """

        if not response["success"]:
            return response

        data = response["data"]

        return {
            "verified": False,
            "transaction_reference": None,
            "gateway_reference": None,
            "amount": None,
            "currency": None,
            "payment_method": None,
            "raw": data,
        }



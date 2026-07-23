


import stripe
from django.conf import settings

from .base import BasePaymentGateway


class StripeGateway(BasePaymentGateway):
    """
    Stripe PaymentIntent implementation.

    Uses Stripe's official Python SDK.
    """

    def __init__(self):
        super().__init__()

        stripe.api_key = settings.STRIPE_SECRET_KEY

    def initialize_payment(self, payment):
        """
        Create a Stripe PaymentIntent.
        """

        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),
            currency=payment.currency.lower(),
            automatic_payment_methods={
                "enabled": True,
            },
            metadata={
                "order_id": str(payment.order.id),
                "payment_id": str(payment.id),
                "user_id": str(payment.user.id),
            },
            description=(
                f"AI_Ecommerce Order #{payment.order.id}"
            ),
        )

        return {
            "success": True,
            "payment_intent_id": intent.id,
            "client_secret": intent.client_secret,
            "status": intent.status,
            "raw": intent,
        }

    def verify_payment(
        self,
        payment_intent_id,
    ):
        """
        Retrieve a PaymentIntent.
        """

        intent = stripe.PaymentIntent.retrieve(
            payment_intent_id
        )

        return self.normalize_verification(
            intent
        )

    def refund_payment(
        self,
        payment_intent_id,
    ):
        """
        Refund a successful payment.
        """

        refund = stripe.Refund.create(
            payment_intent=payment_intent_id
        )

        return {
            "success": True,
            "refund_id": refund.id,
            "status": refund.status,
            "raw": refund,
        }

    def normalize_verification(
        self,
        intent,
    ):
        """
        Convert Stripe's PaymentIntent
        into our application's common format.
        """

        return {
            "verified": (
                intent.status == "succeeded"
            ),
            "transaction_reference": intent.id,
            "gateway_reference": intent.latest_charge,
            "amount": intent.amount / 100,
            "currency": intent.currency.upper(),
            "payment_method": (
                intent.payment_method
            ),
            "status": intent.status,
            "client_secret": (
                intent.client_secret
            ),
            "raw": intent,
        }
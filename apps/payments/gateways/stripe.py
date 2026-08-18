


import stripe
from decimal import Decimal

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

        amount = int(
            Decimal(str(payment.amount)) * Decimal("100")
        )

        intent = stripe.PaymentIntent.create(
            amount=amount,
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

    def verify_payment(self, payment_intent_id):
        """
        Retrieve a PaymentIntent.
        """

        intent = stripe.PaymentIntent.retrieve(
            payment_intent_id
        )

        return self.normalize_verification(intent)

    def refund_payment(self, payment):
        """
        Refund a successful payment.
        """
        
        payment_intent_id=(
            payment.gateway_reference
        )
        
        if not payment_intent_id:
        	raise ValueError(
        	   "stripe payment reference method is missing."
        	)

        refund = stripe.Refund.create(
            payment_intent=payment_intent_id
        )

        return {
            "success": True,
            "refund_id": refund.id,
            "status": refund.status,
            "raw": refund,
        }

    def normalize_verification(self, intent):
        """
        Convert Stripe's PaymentIntent
        into our application's common format.
        """

        latest_charge = getattr(
            intent,
            "latest_charge",
            None,
        )

        payment_method = getattr(
            intent,
            "payment_method",
            None,
        )

        client_secret = getattr(
            intent,
            "client_secret",
            None,
        )

        return {
            "verified": (
                intent.status == "succeeded"
            ),
            "transaction_reference": intent.id,
            "gateway_reference": latest_charge,
            "amount": Decimal(intent.amount) / Decimal("100"),
            "currency": intent.currency.upper(),
            "payment_method": payment_method,
            "status": intent.status,
            "client_secret": client_secret,
            "raw": intent,
        }
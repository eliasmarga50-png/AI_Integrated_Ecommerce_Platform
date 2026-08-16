


"""
Business services for the Payments app.
"""

from decimal import Decimal

from django.db import transaction

from apps.orders.models import Order

from .exceptions import (
    AmountMismatchError,
    CurrencyMismatchError,
    DuplicatePaymentError,
    InvalidPaymentStateError,
    InvalidTransactionError,
)
from .gateways.chapa import ChapaGateway
from .gateways.paypal import PayPalGateway
from .gateways.stripe import StripeGateway
from .gateways.telebirr import TelebirrGateway
from .models import Payment


class PaymentService:
    """
    Coordinates payment processing independently
    of the underlying payment gateway.
    """

    GATEWAYS = {
        "chapa": ChapaGateway,
        "telebirr": TelebirrGateway,
        "stripe": StripeGateway,
        "paypal": PayPalGateway,
    }

    @classmethod
    def get_gateway(cls, provider):
        """
        Return the appropriate gateway instance.
        """

        gateway_class = cls.GATEWAYS.get(
            provider.lower()
        )

        if gateway_class is None:
            raise ValueError(
                f"Unsupported gateway: {provider}"
            )

        return gateway_class()

    @classmethod
    @transaction.atomic
    def initialize_payment(cls, payment):
        """
        Send payment initialization request
        to the selected gateway.
        """

        gateway = cls.get_gateway(
            payment.gateway
        )

        response = gateway.initialize_payment(
            payment
        )
        gateway_reference = (
            response.get("payment_intent_id")
            or response.get("order_id")
            or response.get("gateway_reference")
        )
        if gateway_reference:
        	payment.gateway_reference(
        	   gateway_reference
        	)
        	payment.status=(
        	   Payment.Status.PROCESSING
        	)
        	payment.save(
        	   update_fields=[
        	      "gateway_reference",
        	      "status",
        	      "updated_at",
        	   ]
        	)
        return response

    @classmethod
    @transaction.atomic
    def verify_payment(cls, payment):
        """
        Verify payment with the selected gateway.

        Gateway implementations may return either:

        1. An already-normalized response containing
           ``verified``, ``amount`` and ``currency``.

        2. A raw provider response which must be passed
           through the gateway's normalization method.
        """

        gateway = cls.get_gateway(
            payment.gateway
        )
        
        verification_reference = (
            payment.gateway_reference 
            or payment.transaction_reference
        )

        verification = gateway.verify_payment(
            verification_reference
        )

        # -------------------------------------------------
        # Normalize provider response when necessary.
        # -------------------------------------------------
        #
        # A normalized response already contains "verified".
        # This is also important for tests/mocks because a
        # plain Mock pretends to have arbitrary attributes.
        #
        if not (
            isinstance(verification, dict)
            and "verified" in verification
        ):
            normalize = getattr(
                gateway,
                "normalize_verification",
                None,
            )

            if callable(normalize):
                verification = normalize(
                    verification
                )

        # -------------------------------------------------
        # Gateway verification
        # -------------------------------------------------

        if not isinstance(
            verification,
            dict,
        ):
            raise InvalidTransactionError(
                "Invalid gateway verification response."
            )

        if not verification.get(
            "verified",
            False,
        ):
            raise InvalidTransactionError(
                "Gateway verification failed."
            )

        # -------------------------------------------------
        # Validate local payment data
        # -------------------------------------------------

        cls.validate_payment(
            payment,
            verification,
        )

        # -------------------------------------------------
        # Complete payment
        # -------------------------------------------------

        cls.mark_completed(
            payment,
            gateway_reference=verification.get(
                "gateway_reference"
            ),
        )

        return verification

    @classmethod
    def validate_payment(
        cls,
        payment,
        verification,
    ):
        """
        Validate gateway response
        against local records.
        """

        amount = Decimal(
            str(
                verification["amount"]
            )
        )

        if amount != payment.amount:
            raise AmountMismatchError()

        if (
            verification["currency"]
            != payment.currency
        ):
            raise CurrencyMismatchError()

    @classmethod
    @transaction.atomic
    def mark_completed(
        cls,
        payment,
        gateway_reference=None,
    ):
        """
        Mark payment completed.
        """

        if (
            payment.status
            == Payment.Status.COMPLETED
        ):
            raise InvalidPaymentStateError(
                "Payment already completed."
            )

        payment.gateway_reference = (
            gateway_reference
        )

        payment.status = (
            Payment.Status.COMPLETED
        )

        payment.save(
            update_fields=[
                "gateway_reference",
                "status",
            ]
        )

        order = payment.order

        if order.status == Order.Status.PENDING:
            order.status = Order.Status.CONFIRMED
            order.save(
                update_fields=["status"]
            )

        return payment

    @classmethod
    @transaction.atomic
    def create_payment(
        cls,
        *,
        order,
        user,
        gateway,
    ):
        """
        Create a payment record.
        """
        
        payment_method_map = {
           Payment.Gateway.CHAPA : Payment.PaymentMethod.MOBILE_MONEY,
           Payment.Gateway.TELEBIRR : Payment.PaymentMethod.MOBILE_MONEY,
           Payment.Gateway.STRIPE : Payment.PaymentMethod.CARD,
           Payment.Gateway.PAYPAL : Payment.PaymentMethod.CARD,
        }

        if Payment.objects.filter(
            order=order
        ).exists():
            raise DuplicatePaymentError()

        payment = Payment.objects.create(
            order=order,
            user=user,
            gateway=gateway,
            amount=order.total_amount,
            currency=order.currency,
            payment_method=payment_method_map[gateway],
        )

        return payment

    @classmethod
    def refund_payment(
        cls,
        payment,
    ):
        """
        Delegate refund processing
        to the selected gateway.
        """

        gateway = cls.get_gateway(
            payment.gateway
        )

        return gateway.refund_payment(
            payment
        )
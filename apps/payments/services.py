


"""
Business services for the Payments app.
"""

from decimal import Decimal

from django.db import transaction

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

        gateway_class = cls.GATEWAYS.get(provider.lower())

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

        return gateway.initialize_payment(
            payment
        )

    @classmethod
    @transaction.atomic
    def verify_payment(
        cls,
        payment,
    ):
        """
        Verify payment with the selected gateway.
        """

        gateway = cls.get_gateway(
            payment.gateway
        )

        verification = gateway.verify_payment(
            payment.transaction_reference
        )

        if hasattr(
            gateway,
            "normalize_verification",
        ):
            verification = (
                gateway.normalize_verification(
                    verification
                )
            )

        if not verification["verified"]:
            raise InvalidTransactionError(
                "Gateway verification failed."
            )

        cls.validate_payment(
            payment,
            verification,
        )

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

        if hasattr(order, "status"):
            order.status = "PAID"
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
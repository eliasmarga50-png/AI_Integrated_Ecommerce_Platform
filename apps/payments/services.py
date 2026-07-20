


from decimal import Decimal

from django.db import transaction

from .models import Payment


class PaymentService:
    """
    Handles payment business logic and payment state transitions.
    """

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        user,
        order,
        gateway,
        payment_method,
    ):
        """
        Create a payment for an order.
        """

        if order.user != user:
            raise PermissionError(
                "You do not have permission to pay for this order."
            )

        if hasattr(order, "payment"):
            raise ValueError(
                "A payment already exists for this order."
            )

        if order.total_amount <= Decimal("0.00"):
            raise ValueError(
                "An order with zero amount cannot be paid."
            )

        payment = Payment.objects.create(
            user=user,
            order=order,
            amount=order.total_amount,
            gateway=gateway,
            payment_method=payment_method,
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_processing(payment):
        """
        Mark a pending payment as processing.
        """

        if payment.status != Payment.Status.PENDING:
            raise ValueError(
                "Only pending payments can be marked as processing."
            )

        payment.status = Payment.Status.PROCESSING
        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_completed(
        payment,
        *,
        transaction_reference,
    ):
        """
        Mark a payment as completed after successful gateway verification.
        """

        if payment.status != Payment.Status.PROCESSING:
            raise ValueError(
                "Only processing payments can be completed."
            )

        if not transaction_reference:
            raise ValueError(
                "A transaction reference is required."
            )

        payment.status = Payment.Status.COMPLETED
        payment.transaction_reference = transaction_reference

        payment.save(
            update_fields=[
                "status",
                "transaction_reference",
                "updated_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_failed(payment):
        """
        Mark a processing payment as failed.
        """

        if payment.status != Payment.Status.PROCESSING:
            raise ValueError(
                "Only processing payments can be marked as failed."
            )

        payment.status = Payment.Status.FAILED

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def refund(payment):
        """
        Refund a completed payment.
        """

        if payment.status != Payment.Status.COMPLETED:
            raise ValueError(
                "Only completed payments can be refunded."
            )

        payment.status = Payment.Status.REFUNDED

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return payment



"""
Payment webhook handlers.

This module receives and validates payment notifications
from external payment gateways.
"""

import json

from django.db import transaction
from django.http import JsonResponse

from .exceptions import (
    AmountMismatchError,
    CurrencyMismatchError,
    InvalidTransactionError,
    ReplayAttackError,
    SignatureVerificationError,
)
from .models import Payment
from .services import PaymentService
from .utils import (
    is_timestamp_valid,
    verify_hmac_signature,
)


class PaymentWebhookHandler:
    """
    Handles incoming gateway webhook events.
    """

    def __init__(self, gateway_secret):
        self.gateway_secret = gateway_secret

    @transaction.atomic
    def process_webhook(
        self,
        *,
        payload,
        signature,
        timestamp,
    ):
        """
        Process and validate a payment webhook.
        """

        # 1. Verify timestamp
        if not is_timestamp_valid(timestamp):
            raise ReplayAttackError(
                "Webhook timestamp is expired."
            )

        # 2. Verify signature
        payload_bytes = json.dumps(
            payload,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

        signature_valid = verify_hmac_signature(
            payload=payload_bytes,
            secret=self.gateway_secret,
            received_signature=signature,
        )

        if not signature_valid:
            raise SignatureVerificationError()

        # 3. Extract transaction information
        transaction_id = payload.get(
            "transaction_id"
        )

        amount = payload.get(
            "amount"
        )

        currency = payload.get(
            "currency"
        )

        if not transaction_id:
            raise InvalidTransactionError()

        # 4. Find payment
        try:
            payment = Payment.objects.select_for_update().get(
                transaction_reference=transaction_id
            )

        except Payment.DoesNotExist:
            raise InvalidTransactionError(
                "Payment transaction not found."
            )

        # 5. Confirm amount
        if str(payment.amount) != str(amount):
            raise AmountMismatchError()

        # 6. Confirm currency
        if payment.currency != currency:
            raise CurrencyMismatchError()

        # 7. Prevent duplicate processing
        if payment.status == Payment.Status.COMPLETED:
            raise ReplayAttackError(
                "Payment has already been completed."
            )

        # 8. Complete payment
        PaymentService.mark_completed(
            payment,
            transaction_reference=transaction_id,
        )

        return payment


def payment_webhook_response(
    handler,
    request,
):
    """
    Django view helper for webhook processing.
    """

    try:
        payload = json.loads(
            request.body
        )

        signature = request.headers.get(
            "X-Payment-Signature"
        )

        timestamp = request.headers.get(
            "X-Payment-Timestamp"
        )

        payment = handler.process_webhook(
            payload=payload,
            signature=signature,
            timestamp=timestamp,
        )

        return JsonResponse(
            {
                "status": "success",
                "payment_id": payment.id,
            }
        )

    except Exception as error:

        return JsonResponse(
            {
                "status": "error",
                "message": str(error),
            },
            status=400,
        )
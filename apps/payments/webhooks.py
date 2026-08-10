


"""
Payment webhook handlers.

This module receives and validates payment notifications
from external payment gateways.

Gateway-specific verification protocols should be implemented
by the corresponding gateway integration. This handler provides
the common application-level validation and state-transition
boundary.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone as dt_timezone

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
    Handles incoming payment webhook events.

    The handler is deliberately gateway-aware so a webhook endpoint
    cannot authenticate a transaction for the wrong gateway.
    """

    def __init__(
        self,
        *,
        gateway,
        gateway_secret,
    ):
        if not gateway:
            raise ValueError(
                "A payment gateway is required."
            )

        if not gateway_secret:
            raise ValueError(
                "A webhook secret is required."
            )

        self.gateway = gateway
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
        Validate and process a payment webhook.

        Validation order is intentional:

        1. Validate timestamp.
        2. Validate signature.
        3. Validate transaction reference.
        4. Lock the payment row.
        5. Validate gateway ownership.
        6. Validate amount.
        7. Validate currency.
        8. Reject already-completed payments.
        9. Complete the payment.
        """

        # -------------------------------------------------
        # 1. Verify timestamp
        # -------------------------------------------------

        if not is_timestamp_valid(timestamp):
            raise ReplayAttackError(
                "Webhook timestamp is expired or invalid."
            )

        # -------------------------------------------------
        # 2. Verify signature
        # -------------------------------------------------

        if not signature:
            raise SignatureVerificationError()

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

        # -------------------------------------------------
        # 3. Extract transaction information
        # -------------------------------------------------

        transaction_id = payload.get(
            "transaction_id"
        )

        amount = payload.get("amount")
        currency = payload.get("currency")

        if not transaction_id:
            raise InvalidTransactionError()

        # -------------------------------------------------
        # 4. Find and lock payment
        # -------------------------------------------------

        try:
            payment = (
                Payment.objects
                .select_for_update()
                .select_related("order")
                .get(
                    transaction_reference=transaction_id
                )
            )

        except Payment.DoesNotExist:
            raise InvalidTransactionError(
                "Payment transaction not found."
            )

        # -------------------------------------------------
        # 5. Verify gateway ownership
        # -------------------------------------------------

        if payment.gateway != self.gateway:
            raise InvalidTransactionError(
                "Payment gateway mismatch."
            )

        # -------------------------------------------------
        # 6. Confirm amount
        # -------------------------------------------------

        if str(payment.amount) != str(amount):
            raise AmountMismatchError()

        # -------------------------------------------------
        # 7. Confirm currency
        # -------------------------------------------------

        if payment.currency != currency:
            raise CurrencyMismatchError()

        # -------------------------------------------------
        # 8. Prevent duplicate processing
        # -------------------------------------------------

        if payment.status == Payment.Status.COMPLETED:
            raise ReplayAttackError(
                "Payment has already been completed."
            )

        # -------------------------------------------------
        # 9. Complete payment
        # -------------------------------------------------

        PaymentService.mark_completed(
            payment,
            gateway_reference=transaction_id,
        )

        return payment


def payment_webhook_response(
    handler,
    request,
):
    """
    Django view helper for webhook processing.

    Client responses intentionally expose only a safe,
    generic error message. Internal exception details should
    be logged separately rather than returned to an external
    caller.
    """

    try:
        payload = json.loads(
            request.body
        )

    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid webhook payload.",
            },
            status=400,
        )

    signature = request.headers.get(
        "X-Payment-Signature"
    )

    timestamp = request.headers.get(
        "X-Payment-Timestamp"
    )

    try:
        payment = handler.process_webhook(
            payload=payload,
            signature=signature,
            timestamp=timestamp,
        )

    except (
        AmountMismatchError,
        CurrencyMismatchError,
        InvalidTransactionError,
        ReplayAttackError,
        SignatureVerificationError,
    ):
        return JsonResponse(
            {
                "status": "error",
                "message": "Webhook validation failed.",
            },
            status=400,
        )

    return JsonResponse(
        {
            "status": "success",
            "payment_id": payment.id,
        }
    )
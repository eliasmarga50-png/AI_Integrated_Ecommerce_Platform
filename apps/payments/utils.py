

"""
Utility functions for the Payments app.

These helpers are intentionally stateless and reusable.
They do not access the database or contain business logic.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from datetime import timedelta

from django.utils import timezone


def generate_transaction_reference(prefix: str = "PAY") -> str:
    """
    Generate a unique transaction reference.

    Example:
        PAY-8A2F9C17D4B14E6C
    """
    token = secrets.token_hex(8).upper()
    return f"{prefix}-{token}"


def generate_idempotency_key() -> str:
    """
    Generate an idempotency key.

    This is used when communicating with payment gateways to ensure
    duplicate requests are processed only once.
    """
    return str(uuid.uuid4())


def generate_nonce(length: int = 32) -> str:
    """
    Generate a cryptographically secure random nonce.
    """
    return secrets.token_urlsafe(length)


def calculate_hmac_signature(
    payload: bytes,
    secret: str,
    algorithm=hashlib.sha256,
) -> str:
    """
    Calculate the HMAC signature of a payload.
    """
    return hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=algorithm,
    ).hexdigest()


def verify_hmac_signature(
    payload: bytes,
    secret: str,
    received_signature: str,
) -> bool:
    """
    Verify an HMAC signature using constant-time comparison.
    """
    expected_signature = calculate_hmac_signature(
        payload=payload,
        secret=secret,
    )

    return hmac.compare_digest(
        expected_signature,
        received_signature,
    )


def calculate_payload_hash(
    payload: bytes,
    algorithm=hashlib.sha256,
) -> str:
    """
    Calculate a hexadecimal hash of a payload.
    """
    return algorithm(payload).hexdigest()


def is_timestamp_valid(
    timestamp,
    tolerance_seconds: int = 300,
) -> bool:
    """
    Validate that a timestamp falls within the allowed window.

    Default tolerance is 5 minutes.
    """
    now = timezone.now()

    return abs(now - timestamp) <= timedelta(
        seconds=tolerance_seconds
    )	



"""
Custom exceptions for the Payments app.

Using domain-specific exceptions makes payment errors easier to
understand, log, test, and handle throughout the application.
"""


class PaymentError(Exception):
    """
    Base exception for all payment-related errors.
    """

    default_message = "A payment error occurred."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)


class PaymentValidationError(PaymentError):
    """
    Raised when payment data fails validation.
    """

    default_message = "Payment validation failed."


class PaymentPermissionError(PaymentError):
    """
    Raised when a user attempts an unauthorized payment action.
    """

    default_message = "You do not have permission to perform this payment action."


class DuplicatePaymentError(PaymentError):
    """
    Raised when a payment already exists for an order.
    """

    default_message = "A payment already exists for this order."


class InvalidPaymentStateError(PaymentError):
    """
    Raised when a payment attempts an invalid status transition.
    """

    default_message = "Invalid payment state transition."


class GatewayError(PaymentError):
    """
    Base exception for gateway-related errors.
    """

    default_message = "Payment gateway error."


class GatewayConnectionError(GatewayError):
    """
    Raised when communication with the gateway fails.
    """

    default_message = "Unable to communicate with the payment gateway."


class GatewayTimeoutError(GatewayError):
    """
    Raised when the gateway request times out.
    """

    default_message = "The payment gateway timed out."


class GatewayAuthenticationError(GatewayError):
    """
    Raised when gateway credentials are invalid.
    """

    default_message = "Gateway authentication failed."


class SignatureVerificationError(GatewayError):
    """
    Raised when a webhook or callback signature cannot be verified.
    """

    default_message = "Signature verification failed."


class InvalidTransactionError(GatewayError):
    """
    Raised when a gateway transaction cannot be trusted.
    """

    default_message = "Invalid transaction."


class CurrencyMismatchError(GatewayError):
    """
    Raised when gateway currency does not match the payment.
    """

    default_message = "Currency mismatch detected."


class AmountMismatchError(GatewayError):
    """
    Raised when gateway amount differs from the expected amount.
    """

    default_message = "Amount mismatch detected."


class ReplayAttackError(GatewayError):
    """
    Raised when a transaction has already been processed.
    """

    default_message = "Duplicate transaction detected."


class RefundError(PaymentError):
    """
    Raised when a refund cannot be completed.
    """

    default_message = "Refund failed."
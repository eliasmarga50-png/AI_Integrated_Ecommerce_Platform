


class PaymentError(Exception):
	default_message="Payment error occured."
	def __init__(self, message=None):
		
		super().__init__(message or self.default_message)

class PaymentValidationError(PaymentError):
	
class PaymentPermissionError(PaymentError):
	
class DuplicatePaymentError(PaymentError):
	
class InvalidPaymentStateError(PaymentError):

class GatewayError(PaymentError):

class GatewayConnectionError(PaymentError):
	
class GatewayTimeoutError(PaymentError):
	
class GatewayAuthenticationError(PaymentError):

class SignatureVerificationError(PaymentError):
	
class InvalidTransactionError(PaymentError):
	
class CurrencyMismatchError(PaymentError):
	
class AmountMismatchError(PaymentError):
	
class ReplayAttackError(PaymentError):
	
class RefundError(PaymentError):


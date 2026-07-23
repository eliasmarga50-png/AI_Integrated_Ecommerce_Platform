


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
from .gateways.paypal import PaypalGateway
from .gateways.stripe import StripeGateway
from .gateways.telebirr import TelebirrGateway
from .models import Payment


class PaymentService:
	
	GATEWAYS = {
	    "chapa" : ChapaGateway
	    "telebirr" : TelebirrGateway,
	    "stripe" : StripeGateway,
	    "paypal" : PaypalGateway,
	}
	
	@classmethod
	def get_gateway(
	  cls, 
	  provider
	  ):
	
	@classmethod
	@transaction.atomic
	def initialize_payment(
   	cls, 
   	provider
   	):
		
	
	@classmethod
	@transaction.atomic
	def verify_payment(
	    cls, 
	    payment
	    ):
		
	
	
	@classmethod
	def validate_payment(
	     cls, 
	     payment, 
	     verification
	     ):
		
	@classmethod
	@transaction.atomic
	def mark_completed(
	    cls, 
	    payment, 
	    gateway_reference=None
	    ):
		
	@classmethod
	@transaction.atomic
	def create_payment(
	cls,
	*,
	order,
	user,
	gateway,
	):
	
	
	@classmethod
	def refund(
	   cls,
	   payment,
	):
		
	
	
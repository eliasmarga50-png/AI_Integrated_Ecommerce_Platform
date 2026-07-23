


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
	  	gateway_class = cls.GATEWAYS.get(provider.lower())
	  	
	  	if gateways_class is None:
	  		raise ValueError(f"Unsupported Gateway {provider} ")
	  	
	  	return gateway_class()
	
	@classmethod
	@transaction.atomic
	def initialize_payment(
   	cls, 
   	provider
   	):
   		gateway=cls.get_gateway(
   		   payment.gateway
   		)
   		
   		return gateway.initialize_payment(payment)
		
	
	@classmethod
	@transaction.atomic
	def verify_payment(
	    cls, 
	    payment
	    ):
	    	
	    	gateway=cls.get_gateway(
	    	   payment.gateway
	    	)
	    	
	    	verification=gateway.verify_payment(
	    	   payment.transaction_reference
	    	)
	    	
	    	if hasattr(
	    	   gateway,
	    	   "normalize_verification"
	    	   ):
	    	   	verification=(
	    	   	   gateway.normalize_verification(
	    	   	      verification
	    	   	   )
	    	   )
	    	if not verification["verified"]:
	    		raise InvalidTransactionError(
	    		 "Gateway verification failed. "
	    			)
	    	cls.validate_payment(
	    	   payment,
	    	   verification,
	    		)
	    	cls.mark_completed(
	    	   payment,
	    	   gateway_reference=verification.get(
	    	      "gateway reference"
	    	   )
	    	)
	    	
	    	return verification
	    	
	@classmethod
	def validate_payment(
	     cls, 
	     payment, 
	     verification
	     ):
	     	amount=Decimal(
	     	    str(
	     	       verification["amount"]
	     	    )
	     	)
	     	
	     	if amount != payment.amount:
	     		raise AmountMismatchError()
	     	
	     	if (
	     	   verification["currency"] != amount.curreny
	     	):
	     		raise CurrencyMismatchError():
		
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
		
	
	
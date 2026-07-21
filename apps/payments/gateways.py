


from abc import ABC, abstractmethod

class BasePaymentGateway(ABC):
	
	@abstractmethod
	def initialize_payment(self, payment):
		pass
		
	@abstractmethod
	def verify_payment(self, payment):
		pass
		
class ChapaGateway(BasePaymentGateway):
	
	
	def initialize_payment(self, payment):
		
		return (
		   "status" : "success",
		   "message" : "Payment initialized with Chapa",
		   "payment_id" : payment.id,
		   
		)
		
	def verify_payment(self, payment):
		
		return (
		  "verified" : True,
		  "transaction_reference" : (
		    f"CHAPA - {payment.id}"
		  )
		)

class TelebirrGateway(BasePaymentGateway):
	
	def initialize_payment(self, payment):
		
		return (
		  "status" : "success",
		  "message" : "Payment initialized via Telebirr",
		  "payment_id" : payment.id,
		)
		
	def verify_payment(self, payment):
		
		return (
		  "verified" : True,
		  "transaction_reference" : (
		   f"TELEBIRR - {payment.id} "
		  )
		)
		
class StripeGateway(self, payment):
	
	def initialize_payment(self, payment):
		
		return (
		  "status" : "success",
		  "message" : "Payment initialized via Stripe",
		  "transaction_id" : payment.id
		)
		
	def verify_payment(self, payment):
		
		return (
		  "verified" : True,
		  "transaction_reference" : (
		    f"STRIPE - {payment.id}"
		  )
		)

def get_payment_gateway(gateway_name):
	
	gateways={
	  "CHAPA" : ChapaGateway,
	  "TELEBIRR" : TelebirrGateway,
	  "STRIPE" : StripeGateway
	}
	
	gateway_class = gateways.get(gateway_name)
	
	if not gateway_class:
		raise ValueError(
		  "Unsupported payment gateway"
		)
	
	return gateway_class()


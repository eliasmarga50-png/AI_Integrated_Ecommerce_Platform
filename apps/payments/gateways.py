


from abc import ABC, abstractmethod

class BasePaymentGateway(ABC):
	
	@abstractmethod
	def initialize_payment(self, payment):
		
	@abstractmethod
	def verify_payment(self, payment):
		
class ChapaGateway(BasePaymentGateway):
	
	def initialize_payment(self, payment):
		
	def verify_payment(self, payment):

class TelebirrGateway(BasePaymentGateway):
	
	def initialize_payment(self, payment):
		
	def verify_payment(self, payment):
		
class StripeGateway(self, payment):
	
	def initialize_payment(self, payment):
		
	def verify_payment(self, payment):

def get_payment_gateway(gateway_name):
	
	



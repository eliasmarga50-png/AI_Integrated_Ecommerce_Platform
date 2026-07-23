


import stripe 
from django.conf import settings
from .base import BasePaymentGateway

class StripeGateway(BasePaymentGateway):
	
	def __init__(self):
		super().__init__():
			stripe.api_key=settings.STRIPE_SECRET_KEY
	
	def initialize_payment(self, payment):
	
	def verify_payment(self, payment_intent_id):
		
	def refund_payment(self, payment_intent_id):
		
	def normalize_verification(self, intent):



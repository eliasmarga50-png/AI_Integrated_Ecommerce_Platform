


import stripe 
from django.conf import settings
from .base import BasePaymentGateway

class StripeGateway(BasePaymentGateway):
	
	def __init__(self):
		super().__init__():
			stripe.api_key=settings.STRIPE_SECRET_KEY
	
	def initialize_payment(self, payment):
		intent=stripe.PaymentIntent.create(
		amount=int(payment.amount*100)
		currency=payment.currency.lower()
		automatic_payment_methods = {
		    "enabled" : True
		}
		metadata={
		      "order_id": str(payment.order.id),
		      "payment_id": str(payment.id),
		      "user_id": (payment.user.id),
		}
		description=(
		    f"AI Ecommerce order {payment.order.id}"
		),
		)
		
		return (
		   "success" : True,
		   "payment_intent_id" : intent.id,
		   "client_secret" : intent.client_secret,
		   "status" : intent.status,
		   "raw" : intent,
		)
	
	def verify_payment(self, payment_intent_id):
		intent=stripe.PaymentIntent.retrieve(
		     payment_intent_id
		)
		
		return self.normalize_verification(
		      intent
		)
		
		
	def refund_payment(self, payment_intent_id):
		
		refund=stripe.Refund.create(
		    payment_intent=payment_intent_id
		)
		
		return {
		    "success" : True,
		    "refund_id" : refund.id,
		    "status" : refund.status,
		    "raw" : refund,
		}
		
	def normalize_verification(self, intent):






from paypalserversdk.http.auth.o_auth_2 import ClientCredentialsAuthCredentials 
from paypalsersdk.paypal_serversdk_client import PaypalServersdkClient

from .base import BasePaymentGateway

class PaypalGateway(BasePaymentGateway):
	
	def __init__(self):
		super().__init__()
		
		self.client=PaypalSersdkClient(
		   client_credentials_auth_credentials=ClientCredentialsAuthCredentials
		)
	
	def initialize_payment(self, payment):
	
	
	def verify_payment(self, order_id):
		
	def capture_payment(self, order_id):
	
	
	def refund_payment(self, payment):



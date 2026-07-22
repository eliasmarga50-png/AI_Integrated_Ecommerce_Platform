


import logging
from django.conf import settings

from ..exceptions import (
     GatewayConnectionError,
     GatewayTimeoutError,
     GatewayAuthenticationError,
)

from ..utils import generate_idempotency_key

logger=logging.getLogger(__name__)

class BasePaymentGateway:
	
	base_url
	api_key
	
	timeout
	
	def __init__(
     	self,
     	*,
     	base_url=None,
     	api_key=None):
     
     
     def get_headers(self):
     
     def request():
     	
     def handle_response():
     
     def initialize_payment():
     
     def verify_payment():
     	
     def refund_payment():





import json
from django.db import transaction
from django.http import JsonResponse

from .exceptions import (
    AmountMismatchError,
    CurrencyMismatchError,
    InvalidTransactionError,
    ReplayAttackError,
    SignatureVerificationError,
)

from .models import Payment
from .services import PaymentService
from .utils import (
   is_timestamp_valid,
   verify_hmac_signature,
)


class PaymentWebhookHandler:
	
	def __init__(self, gateway_secret):
		self.gateway_secret=gateway_secret
		
	
	@transaction.atomic
	def process_webhook(
	  self,
	  *,
	  payload,
	  signature,
	  timestamp,
	):


def payment_webhook_response(
      handler,
      request,
):
	try:
		
	except Exception as Error:
		
		return JsonResponse(
		{
		   "status" : "error",
		   "message" : str(error),
		},
		status=400,
		)


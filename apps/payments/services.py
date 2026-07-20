


from decimal import Decimal
from .models import Payment
from django.db import transaction

class PaymentService:
	
	@staticmethod
	@transaction.atomic
	def create_payment(
	   *,
	   user,
	   order,
	   gateway,
	   payment_method):
	   	
	   
	   @staticmethod
	   @transaction.atomic
	   def mark_processing(payment):
	   	
	   
	   @staticmethod
	   @transaction.atomic
	   def mark_completed(
	    payment,
	    *,
	    transaction_difference,
	   ):
	   	
	   
	   @staticmerhod
	   @transaction.atomic
	   def mark_failed(payment):
	   
	   
	   @staticmethod
	   @transaction.atomic
	   def refund(payment):






from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models 

class Payment(models.Model):
	
	class Status(models.TextChoices):
		
	class Gateway(models.TextChoices):
		
	class PaymentMethod(models.TextChoices):
	
	user
	
	order
	
	amount
	
	currency
	
	status
	
	gateway
	
	payment_method
	
	transaction_reference
	
	created_at
	
	updated_at
	
	class Meta:
		ordering=["-created_at"]
		
	def __str__(self):
		
		return (
		   f"Payment  {self.pk} - "
		   f"{self.amount}  {self.currency} - "
		   f"{self.get_status_display()}"
		)



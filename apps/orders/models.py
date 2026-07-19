


from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models 


class order(models.Model):
	
	class status(models.TextChoices):
	
	user=
	
	order_number=
	
	status=
	
	total_amount=
	
	shipping_adress=
	
	shipping_city=
	
	shipping phone=
	
	created_at=
	
	updated_at=
	
	class Meta:
		
		ordering=
	
	def __str__(self):
		
		return self.order_number
		
class OrderItem(models.Model):
	
	order=
	
	product=
	
	product_name=
	
	unit_price=
	
	quantity=
	
	sub_total=
	
	def __str__(self):
		
		return f"{self.product_name} * {self.quantity}"


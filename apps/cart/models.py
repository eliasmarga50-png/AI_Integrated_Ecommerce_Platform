


from django.conf import settings
from django.db import models 
from apps.products.model import Product

class Cart(models.Model):
	
	owner=
	created_at=
	updated_at=
	
	class Meta:
		ordering=
	
	def __str__(self):
		return 
	
	@property
	def total_items(self):
		
	@property
	def total_price(self):
	
	
class CartItem(models.Model):
	
	cart=
	product=
	quantity=
	added_at=
	updated_at=
	
	class Meta:
		
		ordering=
		constraints=
		
	def __str__(self):
	
	
	@property
	def subtotal(self):



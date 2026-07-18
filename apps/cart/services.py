


from .models import Cart, CartItem
from django.db import transaction

class CartService:
	
	@staticmethod
	def get_or_create_cart(user):
		
	
	@staticmethod
	@transaction.atomic
	def add_product(cart, product, quantity=1):
		
	
	@staticmethod
	@transaction.atomic
	def update_quantity(cart, product, quantity):
		
	
	@staticmethod
	@transaction.atomic
	def remove_product(cart, quantity):
		
	
	@staticmethod
	@transaction.atomic
	def clear_cart(cart):
		
	
	@staticmethod
	def get_cart_items(cart):
		
	
	@staticmethod
	def get_cart_summary(cart):
		
	
	



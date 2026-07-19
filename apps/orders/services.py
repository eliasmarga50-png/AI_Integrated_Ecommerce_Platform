


from decimal import Decimal 
from django.db import transaction

from .models import Order, OrderItem
from .utils import generate_random_string()


class OrderService:
	
	@staticmethod
	def calculate_order_total(cart):
		
	
	@staticmethod
	@atomic.method
	def create_order_from_cart(
	      cart,
	      shipping_address,
	      shipping_city,
	      shipping_phone,
	):
		
		order
		
		total_amount
		
		cart_items
		
	
	@staticmethod
	def get_user_orders(user):
		
		
	@staticmethod
	def get_order(order_number, user):






from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from apps.products.models import Product

@login_required
def cart_detail(request)


@login_required
def add_to_cart(request, product_id):
	
@login_required
def update_cart_item(request, product_id):
	
@login_required
def remove_from_cart(request, product_id):
	
@login_required
def clear_cart(request):






from django.contrib.auth.decorators import login_required
from django.contrib import message
from django.shortcuts import get_object_or_404, render, redirect

from .services import OrderService
from .forms import CheckoutForm

@login_required
def order_list(request):
	
@login_required
def order_detail(request, order_number):
	
@login_required
def checkout(request):





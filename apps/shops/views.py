


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms  import ShopCreateForm, ShopUpdateForm
from .models import Shop
from .services import ShopService

@login_required
def shop_list(request):
	
	
@login_required
def shop_create(request):
	

@login_required
def shop_detail(request, slug):
	

@login_required
def shop_update(request, slug):
	

@login_required
def shop_deactivate(request, slug):



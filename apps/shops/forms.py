
from .models import Shop

from django import forms

class ShopCreateForm(forms.ModelForm):
	
	class Meta:
		model=Shop
		
		fields=()
		
		widgets={}
		
	
	def clean_name(self):
	
	
class ShopUpdateForm(forms.ModelForm):
	
	class Meta:
		model=Shop
		
		fields=()
		
		
		widgets={}
	
	def clean_name(self):
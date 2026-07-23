


from decimal import Decimal

from .models import Payment

from django import forms


class PaymentCreateForm(forms.ModelForm):
	
	class Meta:
		model=Payment
		fields= [
		   "gateway",
		]
		
		def clean_gateway(self):


class PaymentGatewaySelectionForm(forms.Form):
	
	gateway
	

class PaymentRefundForm(forms.Form):
	
	amount
	
	reoson
	
	def clean_reoson(self):



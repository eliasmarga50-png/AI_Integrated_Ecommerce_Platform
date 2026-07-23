


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)
from .forms import (
    PaymentCreateForm,
    PaymentRefundForm,
)

from .models import Payment
from .services import PaymentService

from .webhooks import (
     PaymentWebhookHandler,
     payment_webhook_handler,
)


class PaymentListView(LoginRequiredMixin, ListView):
	model=Payment
	template_name="payments/payment_list.html"
	context_payment_name="payments"
	
	def get_queryset(self):
		return (
		   Payment.objects
		   .select_related("order")
		   .filter(user=self.request.user)
		   .order_by("-created_at")
		)
	


class PaymentDetailView(LoginRequiredMixin, DetailView):
	"""
    Display a single payment.
    """

    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"

    def get_queryset(self):
        return (
            Payment.objects
            .select_related("order")
            .filter(user=self.request.user)
        )
	

class PaymentCreateView(LoginRequiredMixin, CreateView):
	

class PaymentInitializeView(LoginRequiredMixin, View):
	

class PaymentVerifyView(LoginRequiredMixin, View):
	

class PaymentRefundView(LoginRequiredMixin, UserPassesTestMixin, View):
	

class PaymentWebhookView(View):


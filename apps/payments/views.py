


"""
Views for the Payments application.
"""

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
    payment_webhook_response,
)


class PaymentListView(LoginRequiredMixin, ListView):
    """
    Display the authenticated user's payments.
    """

    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"

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
    """
    Create a payment record.
    """

    model = Payment
    form_class = PaymentCreateForm
    template_name = "payments/payment_form.html"

    def form_valid(self, form):
        order = self.request.user.orders.get(
            pk=self.kwargs["order_id"]
        )

        payment = PaymentService.create_payment(
            order=order,
            user=self.request.user,
            gateway=form.cleaned_data["gateway"],
        )

        messages.success(
            self.request,
            "Payment created successfully.",
        )

        return redirect(
            "payments:initialize",
            pk=payment.pk,
        )


class PaymentInitializeView(LoginRequiredMixin, View):
    """
    Initialize payment with the selected gateway.
    """

    def post(self, request, pk):
        payment = get_object_or_404(
            Payment,
            pk=pk,
            user=request.user,
        )

        response = PaymentService.initialize_payment(
            payment
        )

        return JsonResponse(response)


class PaymentVerifyView(LoginRequiredMixin, View):
    """
    Verify a payment after gateway processing.
    """

    def post(self, request, pk):
        payment = get_object_or_404(
            Payment,
            pk=pk,
            user=request.user,
        )

        verification = (
            PaymentService.verify_payment(
                payment
            )
        )

        return JsonResponse(verification)


class PaymentRefundView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    View,
):
    """
    Refund a payment.

    Staff users only.
    """

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk):
        payment = get_object_or_404(
            Payment,
            pk=pk,
        )

        form = PaymentRefundForm(request.POST)

        if not form.is_valid():
            return JsonResponse(
                form.errors,
                status=400,
            )

        result = PaymentService.refund_payment(
            payment
        )

        return JsonResponse(result)


class PaymentWebhookView(View):
    """
    Receive payment gateway webhooks.
    """

    http_method_names = ["post"]

    def post(self, request):
        handler = PaymentWebhookHandler(
            gateway_secret="CHANGE_ME"
        )

        return payment_webhook_response(
            handler,
            request,
        )
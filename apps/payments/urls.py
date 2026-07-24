



"""
URL configuration for the Payments application.
"""

from django.urls import path

from .views import (
    PaymentCreateView,
    PaymentDetailView,
    PaymentInitializeView,
    PaymentListView,
    PaymentRefundView,
    PaymentVerifyView,
    PaymentWebhookView,
)

app_name = "payments"

urlpatterns = [

    # -------------------------------------------------
    # Payment pages
    # -------------------------------------------------

    path(
        "",
        PaymentListView.as_view(),
        name="list",
    ),

    path(
        "create/<int:order_id>/",
        PaymentCreateView.as_view(),
        name="create",
    ),

    path(
        "<int:pk>/",
        PaymentDetailView.as_view(),
        name="detail",
    ),

    # -------------------------------------------------
    # Payment actions
    # -------------------------------------------------

    path(
        "<int:pk>/initialize/",
        PaymentInitializeView.as_view(),
        name="initialize",
    ),

    path(
        "<int:pk>/verify/",
        PaymentVerifyView.as_view(),
        name="verify",
    ),

    path(
        "<int:pk>/refund/",
        PaymentRefundView.as_view(),
        name="refund",
    ),

    # -------------------------------------------------
    # Gateway webhooks
    # -------------------------------------------------

    
    ),
    path(
    "webhooks/chapa/",
    PaymentWebhookView.as_view(),
    {"gateway": "chapa"},
    name="chapa-webhook",
),

path(
    "webhooks/stripe/",
    PaymentWebhookView.as_view(),
    {"gateway": "stripe"},
    name="stripe-webhook",
),

path(
    "webhooks/paypal/",
    PaymentWebhookView.as_view(),
    {"gateway": "paypal"},
    name="paypal-webhook",
),

path(
    "webhooks/telebirr/",
    PaymentWebhookView.as_view(),
    {"gateway": "telebirr"},
    name="telebirr-webhook",
),
]



from django.urls import path

from .views import (
    AdminDashboardView,
    CustomerDashboardView,
    SellerDashboardView,
)

app_name = "dashboard"

urlpatterns = [
    path(
        "customer/",
        CustomerDashboardView.as_view(),
        name="customer_dashboard",
    ),
    path(
        "seller/",
        SellerDashboardView.as_view(),
        name="seller_dashboard",
    ),
    path(
        "admin/",
        AdminDashboardView.as_view(),
        name="admin_dashboard",
    ),
]



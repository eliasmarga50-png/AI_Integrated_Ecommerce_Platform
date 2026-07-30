


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .mixins import (
    AdminRequiredMixin,
    CustomerRequiredMixin,
    SellerRequiredMixin,
)
from .services import DashboardService


class CustomerDashboardView(
    LoginRequiredMixin,
    CustomerRequiredMixin,
    View,
):
    template_name = "dashboard/customer/dashboard.html"

    def get(self, request):
        context = DashboardService.get_customer_dashboard(request.user)
        return render(request, self.template_name, context)


class SellerDashboardView(
    LoginRequiredMixin,
    SellerRequiredMixin,
    View,
):
    template_name = "dashboard/seller/dashboard.html"

    def get(self, request):
        context = DashboardService.get_seller_dashboard(request.user)
        return render(request, self.template_name, context)


class AdminDashboardView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    View,
):
    template_name = "dashboard/admin_panel/dashboard.html"

    def get(self, request):
        context = DashboardService.get_admin_dashboard(request.user)
        return render(request, self.template_name, context)


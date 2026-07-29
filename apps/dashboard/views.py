


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .services import DashboardService


class CustomerDashboardView(LoginRequiredMixin, View):
    """
    Display the customer dashboard.
    """

    template_name = "dashboard/customer/dashboard.html"

    def get(self, request):
        context = DashboardService.get_customer_dashboard(request.user)
        return render(request, self.template_name, context)


class SellerDashboardView(LoginRequiredMixin, View):
    """
    Display the seller dashboard.
    """

    template_name = "dashboard/seller/dashboard.html"

    def get(self, request):
        context = DashboardService.get_seller_dashboard(request.user)
        return render(request, self.template_name, context)


class AdminDashboardView(LoginRequiredMixin, View):
    """
    Display the administrator dashboard.
    """

    template_name = "dashboard/admin_panel/dashboard.html"

    def get(self, request):
        context = DashboardService.get_admin_dashboard(request.user)
        return render(request, self.template_name, context)



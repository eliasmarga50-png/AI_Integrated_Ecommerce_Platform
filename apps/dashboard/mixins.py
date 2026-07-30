


from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class DashboardPermissionMixin(UserPassesTestMixin):
    """
    Base class for dashboard permissions.
    """

    raise_exception = True

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(
                "You do not have permission to access this dashboard."
            )

        return super().handle_no_permission()


class CustomerRequiredMixin(DashboardPermissionMixin):

    def test_func(self):
        return self.request.user.is_customer()


class SellerRequiredMixin(DashboardPermissionMixin):

    def test_func(self):
        return self.request.user.is_seller()


class AdminRequiredMixin(DashboardPermissionMixin):

    def test_func(self):
        return self.request.user.is_admin()

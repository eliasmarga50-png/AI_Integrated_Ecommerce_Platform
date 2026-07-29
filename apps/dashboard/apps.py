



from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """
    Configuration for the Dashboard application.

    The dashboard aggregates information from multiple apps
    (orders, products, payments, reviews, shops, and accounts)
    and presents role-specific dashboards for customers,
    sellers, and administrators.

    This class is responsible only for application
    configuration and registration.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    verbose_name = "Dashboard"



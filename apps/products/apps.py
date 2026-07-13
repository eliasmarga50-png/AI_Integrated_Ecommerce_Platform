


from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Application configuration for the Products app.

    This class is responsible for configuring the Products
    application and performing startup initialization.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.products"

    label = "products"

    verbose_name = "Products Management"

    def ready(self):
        """
        Executes once when Django starts.

        This method is the proper place for importing
        signals to avoid circular imports.
        """

        try:
            import apps.products.signals
        except ImportError:
            # signals.py has not been created yet.
            # Ignore during the early stages of development.
            pass
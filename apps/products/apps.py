


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
    	import apps.products.signals
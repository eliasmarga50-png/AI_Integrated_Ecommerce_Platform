


from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Configuration for the Cart application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.cart"

    label = "cart"

    verbose_name = "Shopping Cart"



from django.apps import AppConfig

from django.apps import AppConfig


class ShopsConfig(AppConfig):
    """
    Configuration for the shops application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.shops"

    verbose_name = "Shops"

    def ready(self):
        """
        Application startup configuration.
        """

        pass



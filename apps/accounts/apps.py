


from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for the Accounts application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Accounts"

    def ready(self):
        """
        Import signal handlers when Django starts.
        """
        import apps.accounts.signals
        
        
       
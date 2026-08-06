


from django.apps import AppConfig


class AIConfig(AppConfig):
    """
    Configuration for the AI application.

    This app provides intelligent services for the e-commerce platform,
    including:

    - AI Chatbot
    - Product Recommendations
    - Semantic Search
    - Sentiment Analysis
    - Customer Analytics

    Heavy AI models should NOT be loaded here. Instead, initialize them
    lazily inside the corresponding service modules to avoid slowing
    Django startup.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "ai"

    verbose_name = "AI Services"

    def ready(self):
        """
        Perform application initialization.

        Use this method only for lightweight startup tasks such as:

        - Registering Django signals
        - Initializing caches
        - Scheduling lightweight background setup

        Avoid:
        - Loading ML/LLM models
        - Network requests
        - Expensive computations
        """
        # Future example:
        # from . import signals
        # signals.register()

        pass




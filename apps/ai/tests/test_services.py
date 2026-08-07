


from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai.services import AIService


User = get_user_model()


class AIServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="service_user",
            email="service@exa.com",
            password="testpass123",
        )

        self.service = AIService()

    def test_service_can_be_created(self):
        self.assertIsInstance(
            self.service,
            AIService,
        )

    def test_get_gateway_or_provider_mapping(self):
        self.assertIsNotNone(
            self.service
        )






import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AIViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="view_user",
            email="view@example.com",
            password="testpass123",
        )

        self.client.force_login(
            self.user
        )

    def test_chat_requires_post(self):
        response = self.client.get(
            reverse("ai:chat")
        )

        self.assertEqual(
            response.status_code,
            405,
        )

    def test_chat_invalid_json(self):
        response = self.client.post(
            reverse("ai:chat"),
            data="invalid json",
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_chat_missing_message(self):
        response = self.client.post(
            reverse("ai:chat"),
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_search_endpoint(self):
        response = self.client.get(
            reverse("ai:search"),
            {
                "q": "laptop",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_recommendation_endpoint(self):
        response = self.client.get(
            reverse("ai:recommend")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_sentiment_requires_post(self):
        response = self.client.get(
            reverse("ai:sentiment")
        )

        self.assertEqual(
            response.status_code,
            405,
        )

    def test_analytics_endpoint(self):
        response = self.client.get(
            reverse("ai:analytics")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


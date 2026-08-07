


from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.ai import views


class AIURLTests(SimpleTestCase):

    def test_chat_url(self):
        url = reverse("ai:chat")

        self.assertEqual(
            url,
            "/ai/chat/",
        )

        self.assertEqual(
            resolve(url).func,
            views.chatbot,
        )

    def test_search_url(self):
        url = reverse("ai:search")

        self.assertEqual(
            url,
            "/ai/search/",
        )

        self.assertEqual(
            resolve(url).func,
            views.search,
        )

    def test_recommendation_url(self):
        url = reverse("ai:recommend")

        self.assertEqual(
            url,
            "/ai/recommend/",
        )

        self.assertEqual(
            resolve(url).func,
            views.recommendations,
        )

    def test_sentiment_url(self):
        url = reverse("ai:sentiment")

        self.assertEqual(
            url,
            "/ai/sentiment/",
        )

        self.assertEqual(
            resolve(url).func,
            views.sentiment,
        )

    def test_analytics_url(self):
        url = reverse("ai:analytics")

        self.assertEqual(
            url,
            "/ai/analytics/",
        )

        self.assertEqual(
            resolve(url).func,
            views.analytics,
        )



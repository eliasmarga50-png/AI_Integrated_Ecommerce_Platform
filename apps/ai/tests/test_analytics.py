


from django.contrib.auth import get_user_model
from django.test import TestCase

from ai.analytics import AnalyticsEngine
from ai.models import AIAnalyticsLog


User = get_user_model()


class AnalyticsEngineTests(TestCase):

    def setUp(self):
        self.engine = AnalyticsEngine()

        self.user = User.objects.create_user(
            username="analytics_user",
            password="testpass123",
        )

    def test_record_event(self):
        log = self.engine.record(
            event="chat_response",
            user=self.user,
            metadata={
                "tokens": 150,
            },
        )

        self.assertIsInstance(
            log,
            AIAnalyticsLog,
        )

        self.assertEqual(
            log.event,
            "chat_response",
        )

    def test_record_without_metadata(self):
        log = self.engine.record(
            event="search",
            user=self.user,
        )

        self.assertEqual(
            log.metadata,
            {},
        )

    def test_customer_insights(self):
        result = self.engine.customer_insights(
            self.user
        )

        self.assertIsInstance(
            result,
            dict,
        )

    def test_sales_insights(self):
        result = self.engine.sales_insights()

        self.assertIsInstance(
            result,
            dict,
        )

    def test_search_analytics(self):
        result = self.engine.search_analytics()

        self.assertIsInstance(
            result,
            dict,
        )

    def test_recommendation_analytics(self):
        result = self.engine.recommendation_analytics()

        self.assertIsInstance(
            result,
            dict,
        )

    def test_chatbot_analytics(self):
        result = self.engine.chatbot_analytics()

        self.assertIsInstance(
            result,
            dict,
        )

    def test_sentiment_analytics(self):
        result = self.engine.sentiment_analytics()

        self.assertIsInstance(
            result,
            dict,
        )

    def test_dashboard(self):
        result = self.engine.dashboard()

        self.assertIsInstance(
            result,
            dict,
        )

        self.assertIn(
            "chatbot",
            result,
        )

        self.assertIn(
            "search",
            result,
        )

        self.assertIn(
            "recommendations",
            result,
        )

        self.assertIn(
            "sentiment",
            result,
        )

        self.assertIn(
            "sales",
            result,
        )



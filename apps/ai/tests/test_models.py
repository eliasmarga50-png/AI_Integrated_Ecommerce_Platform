


from django.contrib.auth import get_user_model
from django.test import TestCase

from ai.models import (
    AIAnalyticsLog,
    AIChatMessage,
    AIChatSession,
    RecommendationLog,
    SearchQuery,
    SentimentAnalysis,
)


User = get_user_model()


class AIModelTestMixin:
    """
    Shared setup for AI model tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="ai_test_user",
            password="testpass123",
        )


class AIChatSessionModelTests(AIModelTestMixin, TestCase):

    def test_create_chat_session(self):
        session = AIChatSession.objects.create(
            user=self.user,
            title="Shopping Help",
        )

        self.assertEqual(session.user, self.user)
        self.assertEqual(session.title, "Shopping Help")

    def test_chat_session_has_user(self):
        session = AIChatSession.objects.create(
            user=self.user,
            title="Test Chat",
        )

        self.assertIsNotNone(session.user)

    def test_chat_session_string_representation(self):
        session = AIChatSession.objects.create(
            user=self.user,
            title="Shopping Help",
        )

        self.assertIsInstance(str(session), str)


class AIChatMessageModelTests(AIModelTestMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.session = AIChatSession.objects.create(
            user=self.user,
            title="Shopping Help",
        )

    def test_create_user_message(self):
        message = AIChatMessage.objects.create(
            session=self.session,
            role=AIChatMessage.USER,
            message="Show me laptops.",
        )

        self.assertEqual(
            message.session,
            self.session,
        )

        self.assertEqual(
            message.role,
            AIChatMessage.USER,
        )

    def test_create_assistant_message(self):
        message = AIChatMessage.objects.create(
            session=self.session,
            role=AIChatMessage.ASSISTANT,
            message="Here are some laptops.",
        )

        self.assertEqual(
            message.role,
            AIChatMessage.ASSISTANT,
        )


class AIAnalyticsLogModelTests(AIModelTestMixin, TestCase):

    def test_create_analytics_log(self):
        log = AIAnalyticsLog.objects.create(
            event="chat_response",
            user=self.user,
            metadata={
                "tokens": 100,
            },
        )

        self.assertEqual(
            log.event,
            "chat_response",
        )

        self.assertEqual(
            log.metadata["tokens"],
            100,
        )


class SearchQueryModelTests(AIModelTestMixin, TestCase):

    def test_create_search_query(self):
        search = SearchQuery.objects.create(
            query="gaming laptop",
            user=self.user,
        )

        self.assertEqual(
            search.query,
            "gaming laptop",
        )


class SentimentAnalysisModelTests(AIModelTestMixin, TestCase):

    def test_create_sentiment_analysis(self):
        sentiment = SentimentAnalysis.objects.create(
            user=self.user,
            text="This product is excellent.",
            sentiment="positive",
        )

        self.assertEqual(
            sentiment.sentiment,
            "positive",
        )


class RecommendationLogModelTests(AIModelTestMixin, TestCase):

    def test_create_recommendation_log(self):
        recommendation = RecommendationLog.objects.create(
            user=self.user,
            recommendation_type="personalized",
        )

        self.assertEqual(
            recommendation.user,
            self.user,
        )




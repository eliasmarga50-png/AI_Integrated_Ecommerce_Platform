


"""
Central AI service layer.

This module acts as the single entry point for all AI-related
operations. Views should communicate with this service instead of
calling individual AI modules directly.
"""

from .analytics import AnalyticsEngine
from .chatbot import ChatbotEngine
from .recommendation import RecommendationEngine
from .search import SearchEngine
from .sentiment import SentimentEngine


class AIService:
    """
    Coordinates all AI engines.

    Responsibilities:
    - Chatbot
    - Recommendations
    - Semantic Search
    - Sentiment Analysis
    - Analytics
    """

    def __init__(self):
        self.chatbot = ChatbotEngine()
        self.recommendation = RecommendationEngine()
        self.search = SearchEngine()
        self.sentiment = SentimentEngine()
        self.analytics = AnalyticsEngine()

    # --------------------------------------------------
    # Chatbot
    # --------------------------------------------------

    def chat(self, user, message, session=None):
        """
        Generate a chatbot response.
        """
        return self.chatbot.reply(
            user=user,
            message=message,
            session=session,
        )

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    def recommend_products(self, user, limit=10):
        """
        Return personalized product recommendations.
        """
        return self.recommendation.recommend(
            user=user,
            limit=limit,
        )

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search_products(self, query, user=None):
        """
        Perform semantic product search.
        """
        return self.search.search(
            query=query,
            user=user,
        )

    # --------------------------------------------------
    # Sentiment
    # --------------------------------------------------

    def analyze_sentiment(self, text):
        """
        Analyze text sentiment.
        """
        return self.sentiment.predict(text)

    # --------------------------------------------------
    # Analytics
    # --------------------------------------------------

    def record_event(self, event, user=None, metadata=None):
        """
        Record an analytics event.
        """
        metadata = metadata or {}

        return self.analytics.record(
            event=event,
            user=user,
            metadata=metadata,
        )

    def customer_insights(self, user):
        """
        Return AI-generated customer insights.
        """
        return self.analytics.customer_insights(user)

    def sales_insights(self):
        """
        Return AI-generated sales insights.
        """
        return self.analytics.sales_insights()

    # --------------------------------------------------
    # Combined AI Workflow
    # --------------------------------------------------

    def intelligent_search(self, query, user=None):
        """
        Complete AI search pipeline.

        Steps:
        1. Analyze sentiment
        2. Perform semantic search
        3. Generate recommendations
        4. Record analytics
        """

        sentiment = self.analyze_sentiment(query)

        results = self.search_products(
            query=query,
            user=user,
        )

        recommendations = self.recommend_products(
            user=user,
            limit=5,
        )

        self.record_event(
            event="intelligent_search",
            user=user,
            metadata={
                "query": query,
                "sentiment": sentiment,
            },
        )

        return {
            "query": query,
            "sentiment": sentiment,
            "results": results,
            "recommendations": recommendations,
        }



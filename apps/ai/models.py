



import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class TimestampMixin(models.Model):
    """
    Abstract model that provides created/updated timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AIChatSession(TimestampMixin):
    """
    Stores one conversation between a customer and the AI assistant.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_chat_sessions",
    )

    title = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)

    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-last_activity"]
        verbose_name = "AI Chat Session"
        verbose_name_plural = "AI Chat Sessions"

    def __str__(self):
        return f"{self.user} - {self.title or self.id}"


class AIChatMessage(TimestampMixin):
    """
    Individual messages within a chat session.
    """

    USER = "user"
    ASSISTANT = "assistant"

    ROLE_CHOICES = [
        (USER, "User"),
        (ASSISTANT, "Assistant"),
    ]

    session = models.ForeignKey(
        AIChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    message = models.TextField()

    tokens_used = models.PositiveIntegerField(default=0)

    response_time = models.FloatField(default=0)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role} ({self.created_at:%Y-%m-%d %H:%M})"


class RecommendationLog(TimestampMixin):
    """
    Stores AI recommendation requests.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendation_logs",
    )

    recommendation_type = models.CharField(
        max_length=50,
    )

    recommended_products = models.JSONField(default=list)

    confidence_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.recommendation_type}"


class SearchQuery(TimestampMixin):
    """
    Stores semantic search history.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="search_queries",
    )

    query = models.CharField(max_length=500)

    corrected_query = models.CharField(
        max_length=500,
        blank=True,
    )

    results_count = models.PositiveIntegerField(default=0)

    search_time = models.FloatField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.query


class SentimentAnalysis(TimestampMixin):
    """
    Stores sentiment analysis results.
    """

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

    SENTIMENT_CHOICES = [
        (POSITIVE, "Positive"),
        (NEGATIVE, "Negative"),
        (NEUTRAL, "Neutral"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sentiment_analyses",
    )

    text = models.TextField()

    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
    )

    confidence = models.FloatField(default=0.0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.sentiment


class AIAnalyticsLog(TimestampMixin):
    """
    General-purpose AI analytics events.
    """

    event = models.CharField(max_length=100)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "AI Analytics Log"
        verbose_name_plural = "AI Analytics Logs"

    def __str__(self):
        return self.event



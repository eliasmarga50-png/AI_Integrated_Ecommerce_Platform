


from django.contrib import admin

from .models import (
    AIAnalyticsLog,
    AIChatMessage,
    AIChatSession,
    RecommendationLog,
    SearchQuery,
    SentimentAnalysis,
)


# =====================================================
# AI Chat Message Inline
# =====================================================

class AIChatMessageInline(admin.TabularInline):
    model = AIChatMessage
    extra = 0

    fields = (
        "role",
        "message",
        "tokens_used",
        "response_time",
        "created_at",
    )

    readonly_fields = (
        "role",
        "message",
        "tokens_used",
        "response_time",
        "created_at",
    )

    can_delete = False

    ordering = ("created_at",)


# =====================================================
# AI Chat Session
# =====================================================

@admin.register(AIChatSession)
class AIChatSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "title",
        "is_active",
        "last_activity",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "last_activity",
    )

    search_fields = (
        "user__username",
        "title",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "last_activity",
    )

    ordering = ("-last_activity",)

    inlines = [
        AIChatMessageInline,
    ]


# =====================================================
# AI Chat Message
# =====================================================

@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        "session",
        "role",
        "tokens_used",
        "response_time",
        "created_at",
    )

    list_filter = (
        "role",
        "created_at",
    )

    search_fields = (
        "message",
        "session__user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


# =====================================================
# Recommendation Logs
# =====================================================

@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "recommendation_type",
        "confidence_score",
        "created_at",
    )

    list_filter = (
        "recommendation_type",
        "created_at",
    )

    search_fields = (
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


# =====================================================
# Search Queries
# =====================================================

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):

    list_display = (
        "query",
        "user",
        "results_count",
        "search_time",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "query",
        "corrected_query",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


# =====================================================
# Sentiment Analysis
# =====================================================

@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "sentiment",
        "confidence",
        "created_at",
    )

    list_filter = (
        "sentiment",
        "created_at",
    )

    search_fields = (
        "text",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


# =====================================================
# AI Analytics
# =====================================================

@admin.register(AIAnalyticsLog)
class AIAnalyticsLogAdmin(admin.ModelAdmin):

    list_display = (
        "event",
        "user",
        "created_at",
    )

    list_filter = (
        "event",
        "created_at",
    )

    search_fields = (
        "event",
        "user__username",
    )

    readonly_fields = (
        "metadata",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)



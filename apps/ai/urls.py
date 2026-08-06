


"""
URL configuration for AI services.
"""

from django.urls import path

from . import views

app_name = "ai"

urlpatterns = [

    # -----------------------------------------
    # Chatbot
    # -----------------------------------------

    path(
        "chat/",
        views.chatbot,
        name="chat",
    ),

    # -----------------------------------------
    # Search
    # -----------------------------------------

    path(
        "search/",
        views.search,
        name="search",
    ),

    # -----------------------------------------
    # Recommendations
    # -----------------------------------------

    path(
        "recommend/",
        views.recommendations,
        name="recommend",
    ),

    # -----------------------------------------
    # Sentiment Analysis
    # -----------------------------------------

    path(
        "sentiment/",
        views.sentiment,
        name="sentiment",
    ),

    # -----------------------------------------
    # Analytics Dashboard
    # -----------------------------------------

    path(
        "analytics/",
        views.analytics,
        name="analytics",
    ),
]



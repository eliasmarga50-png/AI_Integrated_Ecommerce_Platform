


"""
Views for AI services.
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse

from .services import AIService

ai_service = AIService()


# --------------------------------------------------
# Chatbot
# --------------------------------------------------

@login_required
@require_POST
def chatbot(request):
    """
    AI chatbot endpoint.
    """
    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Message is required.",
                },
                status=400,
            )

        response = ai_service.chat(
            user=request.user,
            message=message,
        )

        return JsonResponse(
            {
                "success": True,
                "message": response.message,
                "tokens_used": response.tokens_used,
                "response_time": response.response_time,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON.",
            },
            status=400,
        )


# --------------------------------------------------
# Search
# --------------------------------------------------

@require_GET
def search(request):
    """
    AI search endpoint.
    """
    query = request.GET.get("q", "").strip()
    
    
    if not query:
        return JsonResponse(
            {
                "success": True,
                "query": "",
                "results": [],
            }
        )

    
    user = request.user if request.user.is_authenticated else None

    results = ai_service.search_products(
        query=query,
        user=user,
    )

    return JsonResponse(
        {
            "success": True,
            "query": query,
            "results": results,
        }
    )


# --------------------------------------------------
# Recommendation
# --------------------------------------------------

@login_required
@require_GET
def recommendations(request):
    """
    Personalized recommendations.
    """
    products = ai_service.recommend_products(
        request.user,
    )

    return JsonResponse(
        {
            "success": True,
            "recommendations": products,
        }
    )


# --------------------------------------------------
# Sentiment
# --------------------------------------------------

@login_required
@require_POST
def sentiment(request):
    """
    Analyze text sentiment.
    """
    try:
        data = json.loads(request.body)
        text = data.get("text", "").strip()

        # FIX: Prevent empty strings from hitting your AI engine
        if not text:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Text is required.",
                },
                status=400,
            )

        result = ai_service.analyze_sentiment(text)

        return JsonResponse(
            {
                "success": True,
                "result": result,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON.",
            },
            status=400,
        )


# --------------------------------------------------
# Dashboard Analytics
# --------------------------------------------------

@login_required
@require_GET
def analytics(request):
    """
    AI dashboard analytics.
    """
    dashboard = ai_service.analytics.dashboard()

    return JsonResponse(
        {
            "success": True,
            "analytics": dashboard,
        }
    )
    

# --------------------------------------------------
# Helpers
# --------------------------------------------------

def serialize_product(product):
    """
    Helper function to transform product data for JSON.
    """
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "url": reverse(
            "products:detail", 
            kwargs={
                "slug": product.slug,
            },
        ),
        "price": str(product.price),
        "description": product.description,
        "category": (
            product.category.name
            if product.category
            else None
        ),
    }

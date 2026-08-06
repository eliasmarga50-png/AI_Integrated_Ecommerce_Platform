


"""
Centralized prompt templates for the AI application.

All LLM prompts should be defined here instead of being embedded
inside chatbot.py, recommendation.py, search.py, or analytics.py.
"""


class PromptLibrary:
    """
    Collection of reusable prompt templates.
    """

    SYSTEM_PROMPT = """
You are the official AI assistant for AI_Ecommerce.

Your responsibilities include:

- Helping customers discover products
- Answering product questions
- Explaining order status
- Assisting with shops and sellers
- Recommending relevant products
- Providing clear and concise answers

Rules:

- Be professional.
- Be friendly.
- Never invent product information.
- If information is unavailable, say so honestly.
- Keep answers concise unless more detail is requested.
""".strip()

    PRODUCT_RECOMMENDATION = """
Recommend products for the following customer.

Customer Profile:
{customer}

Requirements:

- Prioritize relevance.
- Explain each recommendation briefly.
- Avoid duplicate products.
- Prefer in-stock products.
""".strip()

    PRODUCT_SEARCH = """
The customer searched for:

"{query}"

Understand the intent.

Return:

- corrected search terms if needed
- important keywords
- product categories
- possible filters
""".strip()

    SENTIMENT_ANALYSIS = """
Analyze the sentiment of the following review.

Review:

{text}

Return:

- sentiment
- confidence
- short explanation
""".strip()

    SALES_ANALYTICS = """
Analyze the sales data.

Provide:

- trends
- best sellers
- weak-performing products
- opportunities
- concise summary
""".strip()

    CHAT_SUMMARY = """
Summarize this conversation.

Conversation:

{conversation}

Return:

- summary
- important topics
- unresolved issues
""".strip()


def build_prompt(template: str, **kwargs) -> str:
    """
    Safely format a prompt template.

    Example:
        build_prompt(
            PromptLibrary.PRODUCT_SEARCH,
            query="gaming laptop"
        )
    """
    return template.format(**kwargs)



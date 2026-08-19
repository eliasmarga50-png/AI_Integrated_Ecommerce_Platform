

"""
Search engine.

Responsible for intelligent product searching.

The engine is intentionally modular so it can evolve from
simple keyword searching to AI-powered semantic search.
"""

from django.db.models import Q

from apps.products.models import Product
from .utils import normalize_text, remove_duplicate_items
from .prompts import PromptLibrary
from .models import SearchQuery
from .utils import (
    calculate_execution_time,
    start_timer,
)


class SearchEngine:
    """
    AI Search Engine.
    """
    
    def __init__(self, provider=None):
        self.provider = provider

    def search(
        self,
        query,
        user=None,
        limit=20,
    ):
        """
        Main search entry point.
        """
        # Start the clock to measure how fast this specific search runs
        timer = start_timer()

        query = normalize_text(query)

        corrected_query = self.correct_spelling(query)

        results = []

        results.extend(
            self.keyword_search(corrected_query)
        )

        results.extend(
            self.semantic_search(corrected_query)
        )

        results.extend(
            self.category_search(corrected_query)
        )

        results = remove_duplicate_items(results)

        results = self.rank_results(
            results,
            corrected_query,
        )

        # Cut the results to the requested limit
        results = results[:limit]

        # Log the search in the database if a user is logged in
        if user is not None:
            SearchQuery.objects.create(
                user=user,
                query=query,
                corrected_query=corrected_query,
                results_count=len(results),
                search_time=calculate_execution_time(timer),
            )

        return results

    # --------------------------------------------------
    # Keyword Search
    # --------------------------------------------------

    def keyword_search(
        self,
        query,
    ):
        """
        Standard database keyword search.
        """
        if not query:
            return []
        
        return list(
           Product.objects
           .filter(
              is_available=True,
           )
           .filter(
              Q(name__icontains=query)
              |  Q(description__icontains=query)
              |  Q(category__name__icontains=query)
           )
           .select_related("category")
           .distinct()
        )

    # --------------------------------------------------
    # Semantic Search
    # --------------------------------------------------

    def semantic_search(
        self,
        query,
    ):
        """
        AI semantic search.

        Future:
        - Embeddings
        - Vector database
        - Similarity search
        """
        return []

    # --------------------------------------------------
    # Category Search
    # --------------------------------------------------

    def category_search(
        self,
        query,
    ):
        """
        Search inside categories.
        """
        if not query:
            return []
        
        return list(
           Product.objects
           .filter(
              is_available=True,
              category__name__icontains=query,
           )
           .select_related("category")
           .distinct()
        )

    # --------------------------------------------------
    # Spell Correction
    # --------------------------------------------------

    def correct_spelling(self, query):
        """
        Correct spelling using AI provider.
        """
        if not query or self.provider is None:
            return query

        try:
            result = self.provider.generate_json(
                PromptLibrary.PRODUCT_SEARCH.format(
                    query=query
                ),
                system_instruction=(
                    "Return valid JSON only."
                ),
            )

            corrected = result.get(
                "corrected_search_terms"
            )

            if isinstance(
                corrected,
                str,
            ) and corrected.strip():
                return corrected.strip()

            keywords = result.get(
                "keywords",
                []
            )

            if isinstance(
                keywords,
                list
            ) and keywords:
                return " ".join(
                    str(x)
                    for x in keywords
                )

        except Exception:
            pass

        return query

    def detect_intent(
        self,
        query,
    ):
        """
        Detect user search intent.
        """
        return "product"

    # --------------------------------------------------
    # Ranking
    # --------------------------------------------------

    def rank_results(
        self,
        products,
        query,
    ):
        """
        Rank search results.
        """
        return products

    # --------------------------------------------------
    # Filtering
    # --------------------------------------------------

    def filter_results(
        self,
        products,
        **filters,
    ):
        """
        Apply optional filters.
        """
        return products

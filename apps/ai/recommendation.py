


"""
Recommendation engine.

Responsible for generating product recommendations using
multiple recommendation strategies.
"""


from django.db.models import Count
from .models import RecommendationLog

from apps.products.models import Product
from .utils import remove_duplicate_items


class RecommendationEngine:
    """
    AI Recommendation Engine.
    """

    def recommend(self, user=None, limit=10):
        """
        Main recommendation entry point.
        """

        recommendations = []

        recommendations.extend(
            self.personalized(user)
        )

        recommendations.extend(
            self.popular()
        )

        recommendations.extend(
            self.trending()
        )

        recommendations = remove_duplicate_items(
            recommendations
        )
        
        # Fixed: Log is now correctly aligned inside the function
        RecommendationLog.objects.create(
            user=user,
            recommendation_type="mixed",
            recommended_products=[
                product.id
                for product in recommendations
            ],
        )

        return recommendations[:limit]

    # --------------------------------------------------
    # Personalized
    # --------------------------------------------------

    def personalized(self, user, limit=10):

        if user is None:
            return []

        purchased_categories = (
            Product.objects
            .filter(
                order_items__order__user=user,
            )
            .values(
                "category_id"
            )
            .annotate(
                purchases=Count(
                    "order_items"
                )
            )
            .order_by(
                "-purchases"
            )
            .values_list(
                "category_id",
                flat=True,
            )
        )

        category_ids = list(
            purchased_categories[:5]
        )

        if not category_ids:
            return []

        return list(
            Product.objects
            .filter(
                is_available=True,
                category_id__in=category_ids,
            )
            .exclude(
                order_items__order__user=user
            )
            .select_related("category")
            .distinct()
            .order_by("-created_at")[:limit]
        )

    def similar_products(
        self,
        product,
        limit=6,
    ):
        """
        Return products similar to the given product.
        """

        # Placeholder

        return []

    # --------------------------------------------------
    # Frequently Bought Together
    # --------------------------------------------------

    def frequently_bought_together(
        self,
        product,
        limit=4,
    ):
        """
        Return products often purchased together.
        """

        # Placeholder

        return []

    # --------------------------------------------------
    # Trending
    # --------------------------------------------------

    def trending(
        self,
        limit=10,
    ):
        """
        Return trending products.
        """

        # Placeholder

        return []

    # --------------------------------------------------
    # Popular
    # --------------------------------------------------

    def popular(
        self,
        limit=10,
    ):
        """
        Return globally popular products.
        """

        return list(
           Product.objects
           .filter(is_available=True)
           .annotate(
              purchase_count=Count(
                  "order_items"
              )
           )
           .order_by(
              "-purchase_count",
              "-created_at"
           )[:limit]
        )

    # --------------------------------------------------
    # Recently Viewed
    # --------------------------------------------------

    def recently_viewed(
        self,
        user,
        limit=10,
    ):
        """
        Recommend based on recently viewed products.
        """

        if user is None:
            return []

        # Placeholder

        return []

    # --------------------------------------------------
    # New Arrivals
    # --------------------------------------------------

    def new_arrivals(
        self,
        limit=10,
    ):
        """
        Recommend newly added products.
        """

        return list(
           Product.objects
           .filter(is_available=True)
           .order_by("-created_at")[:limit]
        )

    # --------------------------------------------------
    # Ranking
    # --------------------------------------------------

    def rank(
        self,
        products,
    ):
        """
        Final ranking algorithm.
        """

        return products

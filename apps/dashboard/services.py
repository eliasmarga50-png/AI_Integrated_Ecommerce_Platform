


"""
Business logic for the Dashboard application.

The dashboard aggregates information from the rest of the
AI_Ecommerce system. It never owns business data—it simply
collects and prepares it for presentation.
"""

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.products.models import Product
from apps.reviews.models import Review
from apps.shops.models import Shop


User = get_user_model()


class DashboardService:
    """
    Collects dashboard data for different user roles.
    """

    @staticmethod
    def get_customer_dashboard(user):
        return {
            "user": user,
            "recent_orders": DashboardService._get_recent_orders(user),
            "recent_reviews": DashboardService._get_recent_reviews(user),
        }

    @staticmethod
    def get_seller_dashboard(user):
        shop = DashboardService._get_shop(user)

        return {
            "user": user,
            "shop": shop,
            "products": DashboardService._get_products(shop),
        }

    @staticmethod
    def get_admin_dashboard(user):
        return {
            "user": user,
            "total_users": User.objects.count(),
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "total_reviews": Review.objects.count(),
            "total_payments": Payment.objects.count(),
            "total_shops": Shop.objects.count(),
            "revenue": DashboardService._get_total_revenue(),
        }

    # --------------------------------------------------
    # Customer helpers
    # --------------------------------------------------

    @staticmethod
    def _get_recent_orders(user):
        return (
            Order.objects
            .filter(user=user)
            .select_related()
            .order_by("-created_at")[:5]
        )

    @staticmethod
    def _get_recent_reviews(user):
        return (
            Review.objects
            .filter(user=user)
            .select_related("product")
            .order_by("-created_at")[:5]
        )

    # --------------------------------------------------
    # Seller helpers
    # --------------------------------------------------

    @staticmethod
    def _get_shop(user):
        return Shop.objects.filter(owner=user).first()

    @staticmethod
    def _get_products(shop):
        if shop is None:
            return Product.objects.none()

        return (
            Product.objects
            .filter(shop=shop)
            .select_related("category", "shop")
            .order_by("-created_at")
        )

    # --------------------------------------------------
    # Admin helpers
    # --------------------------------------------------

    @staticmethod
    def _get_total_revenue():
        return (
            Payment.objects
            .filter(status="completed")
            .aggregate(
                total=Coalesce(
                    Sum("amount"),
                    0,
                )
            )["total"]
        )



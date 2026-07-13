


import django_filters
from django.db.models import Avg, Q

from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    Advanced product filtering.
    """

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
    )

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
    )

    in_stock = django_filters.BooleanFilter(
        method="filter_stock",
    )

    minimum_rating = django_filters.NumberFilter(
        method="filter_rating",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("price", "price"),
            ("created_at", "created_at"),
            ("name", "name"),
        ),
        field_labels={
            "price": "Price",
            "created_at": "Newest",
            "name": "Product Name",
        },
    )

    class Meta:
        model = Product

        fields = [
            "category",
            "is_available",
        ]

    def filter_search(self, queryset, name, value):
        """
        Search by product name or description.
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_stock(self, queryset, name, value):
        """
        Filter products that have stock.
        """
        if value:
            return queryset.filter(stock__gt=0)

        return queryset.filter(stock=0)

    def filter_rating(self, queryset, name, value):
        """
        Filter by average review rating.
        """
        return (
            queryset
            .annotate(
                average_rating=Avg("reviews__rating")
            )
            .filter(
                average_rating__gte=value
            )
        )



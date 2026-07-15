


import django_filters

from django.db.models import Avg, Q

from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    Advanced product filtering.

    Supports:
    - Product name filtering
    - Full-text style search
    - Category filtering
    - Price range filtering
    - Availability filtering
    - Stock filtering
    - Rating filtering
    - Product ordering
    """

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Product Name",
    )

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
    )

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Minimum Price",
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Maximum Price",
    )

    category = django_filters.ModelChoiceFilter(
        field_name="category",
        queryset=Product._meta.get_field(
            "category"
        ).remote_field.model.objects.all(),
        label="Category",
    )

    in_stock = django_filters.BooleanFilter(
        method="filter_stock",
        label="In Stock",
    )

    minimum_rating = django_filters.NumberFilter(
        method="filter_rating",
        label="Minimum Rating",
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
            "name",
            "category",
            "is_available",
        ]

    def filter_search(self, queryset, name, value):
        """
        Search by product name or description.
        """

        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
        )

    def filter_stock(self, queryset, name, value):
        """
        Filter products based on stock.
        """

        if value is True:
            return queryset.filter(
                stock__gt=0
            )

        if value is False:
            return queryset.filter(
                stock=0
            )

        return queryset

    def filter_rating(self, queryset, name, value):
        """
        Filter by average product rating.
        """

        return (
            queryset
            .annotate(
                average_rating=Avg(
                    "reviews__rating"
                )
            )
            .filter(
                average_rating__gte=value
            )
        )
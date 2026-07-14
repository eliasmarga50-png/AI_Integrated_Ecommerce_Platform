

import logging

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Product

logger = logging.getLogger(__name__)


class ProductService:
    """
    Handles all business logic related to products.

    Future Improvements
    -------------------
    - Inventory management
    - SKU generation
    - Search indexing
    - Product recommendations
    - Cache management
    - Marketplace synchronization
    - Analytics
    - Audit logging
    """

    @staticmethod
    def handle_product_saved(product, created):
        """
        Execute business logic after a product has been saved.
        """

        if created:
            logger.info(
                "Product created: %s",
                product.name,
            )

            # Future:
            # create_inventory(product)
            # generate_default_images(product)
            # send_admin_notification(product)
            # index_product(product)
            # create_product_statistics(product)

        else:
            logger.info(
                "Product updated: %s",
                product.name,
            )

            # Future:
            # clear_product_cache(product)
            # update_search_index(product)
            # sync_marketplace(product)
            # notify_followers(product)

        return product

    @staticmethod
    def get_product(slug):
        """
        Return a single available product.
        """

        return get_object_or_404(
            Product.objects.select_related(
                "category"
            ).prefetch_related(
                "images",
                "reviews",
            ),
            slug=slug,
            is_available=True,
        )

    @staticmethod
    @transaction.atomic
    def create_product(form):
        """
        Create a new product.
        """

        product = form.save()

        logger.info(
            "Product created: %s",
            product.name,
        )

        ProductService.handle_product_saved(
            product,
            created=True,
        )

        return product

    @staticmethod
    @transaction.atomic
    def update_product(form):
        """
        Update an existing product.
        """

        product = form.save()

        logger.info(
            "Product updated: %s",
            product.name,
        )

        ProductService.handle_product_saved(
            product,
            created=False,
        )

        return product

    @staticmethod
    @transaction.atomic
    def delete_product(product):
        """
        Delete a product.
        """

        product_name = product.name

        product.delete()

        logger.warning(
            "Product deleted: %s",
            product_name,
        )

        # Future:
        # archive_product(product)
        # remove_search_index(product)
        # remove_product_images(product)
        # notify_admin(product)

    @staticmethod
    def available_products():
        """
        Return all available products.
        """

        return (
            Product.objects.filter(
                is_available=True
            )
            .select_related("category")
            .prefetch_related(
                "images",
                "reviews",
            )
        )

    @staticmethod
    def products_by_category(category):
        """
        Return products belonging to one category.
        """

        return (
            Product.objects.filter(
                category=category,
                is_available=True,
            )
            .select_related("category")
            .prefetch_related(
                "images",
                "reviews",
            )
        )

    @staticmethod
    def search_products(query):
        """
        Search products.

        Future:
        - Search SKU
        - Search brand
        - Search tags
        - Elasticsearch
        """

        return (
            Product.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query),
                is_available=True,
            )
            .select_related("category")
            .prefetch_related(
                "images",
                "reviews",
            )
            .distinct()
        )

    @staticmethod
    @transaction.atomic
    def update_stock(product, quantity):
        """
        Reduce product stock.
        """

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        if product.stock < quantity:
            raise ValueError(
                "Not enough stock available."
            )

        product.stock -= quantity

        if product.stock == 0:
            product.is_available = False

        product.save(
            update_fields=[
                "stock",
                "is_available",
            ]
        )

        logger.info(
            "Stock updated for %s",
            product.name,
        )

        return product

    @staticmethod
    @transaction.atomic
    def restock_product(product, quantity):
        """
        Increase product stock.
        """

        if quantity <= 0:
            raise ValueError(
                "Quantity must be positive."
            )

        product.stock += quantity
        product.is_available = True

        product.save(
            update_fields=[
                "stock",
                "is_available",
            ]
        )

        logger.info(
            "Product restocked: %s",
            product.name,
        )

        return product



import logging

from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Product

logger = logging.getLogger(__name__)


class ProductService:
    """
    Handles all business logic related to products.
    """

    @staticmethod
    def get_product(slug):
        """
        Return an available product.
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

        # Future:
        # create_inventory(product)
        # generate_sku(product)
        # send_admin_notification(product)

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

    @staticmethod
    def available_products():
        """
        Return all available products.
        """
        return Product.objects.filter(
            is_available=True
        ).select_related(
            "category"
        )

    @staticmethod
    def products_by_category(category):
        """
        Return products in a category.
        """
        return Product.objects.filter(
            category=category,
            is_available=True,
        )

    @staticmethod
    def search_products(query):
        """
        Search products by name.
        """
        return Product.objects.filter(
            name__icontains=query,
            is_available=True,
        )

    @staticmethod
    def update_stock(product, quantity):
        """
        Reduce stock after an order.
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

        product.save()

        logger.info(
            "Stock updated for %s",
            product.name,
        )

        return product

    @staticmethod
    def restock_product(product, quantity):
        """
        Increase stock.
        """
        if quantity <= 0:
            raise ValueError(
                "Quantity must be positive."
            )

        product.stock += quantity
        product.is_available = True

        product.save()

        logger.info(
            "Product restocked: %s",
            product.name,
        )

        return product



import logging

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Product
from .utils import generate_sku, generate_slug
from .services import ProductService


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Product)
def prepare_product(sender, instance, **kwargs):
    """
    Prepare product before saving.
    """

    if not instance.slug:
        instance.slug = generate_slug(
            instance.name
        )

    # Future field
    if hasattr(instance, "sku") and not instance.sku:
        if not instance.sku:
            instance.sku = generate_sku(
                instance.category.name,
                instance.name,
            )

    if instance.stock <= 0:
        instance.is_available = False


@receiver(post_save, sender=Product)
def after_product_saved(
    sender,
    instance,
    created,
    **kwargs,
):
    """
    Handle product lifecycle events
    after a product is saved.
    """

    ProductService.handle_product_saved(
        instance,
        created=created,
    )


@receiver(post_delete, sender=Product)
def after_product_deleted(
    sender,
    instance,
    **kwargs,
):
    """
    Handle product deletion.
    """

    logger.warning(
        "Product deleted: %s",
        instance.name,
    )

    # Future:
    # remove_product_images(instance)
    # delete_search_index(instance)
    # archive_product(instance)
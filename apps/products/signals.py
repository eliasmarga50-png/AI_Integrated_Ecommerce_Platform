


import logging

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Product
from .utils import generate_sku, generate_slug

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
        instance.sku = generate_sku(
            instance.category.name,
            instance.name,
        )

    if instance.stock <= 0:
        instance.is_available = False
    else:
        instance.is_available = True


@receiver(post_save, sender=Product)
def after_product_saved(sender, instance, created, **kwargs):
    """
    Execute actions after saving a product.
    """

    if created:
        logger.info(
            "New product created: %s",
            instance.name,
        )

        # Future:
        # create_inventory(instance)
        # notify_admin(instance)
        # create_search_index(instance)
        # generate_thumbnail(instance)

    else:
        logger.info(
            "Product updated: %s",
            instance.name,
        )

        # Future:
        # clear_product_cache(instance)
        # update_search_index(instance)
        # sync_marketplace(instance)


@receiver(post_delete, sender=Product)
def after_product_deleted(sender, instance, **kwargs):
    """
    Execute actions after deleting a product.
    """

    logger.warning(
        "Product deleted: %s",
        instance.name,
    )

    # Future:
    # remove_product_images(instance)
    # delete_search_index(instance)
    # archive_product(instance)

@receiver(post_save, sender=Product)
def after_product_saved(sender, instance, created, **kwargs):
    ProductService.handle_product_saved(
        instance,
        created=created,
    )
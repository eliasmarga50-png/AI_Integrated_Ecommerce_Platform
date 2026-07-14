


import re

from django.core.exceptions import ValidationError
from django.utils.text import slugify


def validate_product_name(name):
    """
    Validate the product name.
    """
    if not name:
        raise ValidationError(
            "Product name is required."
        )

    if len(name.strip()) < 3:
        raise ValidationError(
            "Product name must contain at least 3 characters."
        )

    if len(name) > 255:
        raise ValidationError(
            "Product name cannot exceed 255 characters."
        )

    return name.strip()


def validate_price(price):
    """
    Validate product price.
    """
    if price is None:
        raise ValidationError(
            "Price is required."
        )

    if price <= 0:
        raise ValidationError(
            "Price must be greater than zero."
        )

    return price


def validate_stock(stock):
    """
    Validate inventory quantity.
    """
    if stock < 0:
        raise ValidationError(
            "Stock cannot be negative."
        )

    return stock


def validate_rating(rating):
    """
    Validate customer review rating.
    """
    if rating < 1 or rating > 5:
        raise ValidationError(
            "Rating must be between 1 and 5."
        )

    return rating


def validate_discount(discount):
    """
    Validate discount percentage.
    """
    if discount < 0 or discount > 100:
        raise ValidationError(
            "Discount must be between 0 and 100 percent."
        )

    return discount


def validate_slug(name):
    """
    Generate and validate slug.
    """
    slug = slugify(name)

    if not slug:
        raise ValidationError(
            "Unable to generate a valid slug."
        )

    return slug


def validate_sku(sku):
    """
    Validate SKU format.

    Example:
    ELE-LAP-AB12CD
    """
    pattern = r"^[A-Z]{3}-[A-Z]{3}-[A-Z0-9]{6}$"

    if not re.match(pattern, sku):
        raise ValidationError(
            "Invalid SKU format."
        )

    return sku


def validate_image_extension(image):
    """
    Validate uploaded image type.
    """
    allowed_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    filename = image.name.lower()

    if not filename.endswith(allowed_extensions):
        raise ValidationError(
            "Only JPG, JPEG, PNG and WEBP images are allowed."
        )

    return image


def validate_image_size(image):
    """
    Validate uploaded image size.

    Maximum:
    5 MB
    """
    max_size = 5 * 1024 * 1024

    if image.size > max_size:
        raise ValidationError(
            "Image size cannot exceed 5 MB."
        )

    return image


def validate_description(description):
    """
    Validate product description.
    """
    if len(description.strip()) < 20:
        raise ValidationError(
            "Description should contain at least 20 characters."
        )

    return description.strip()
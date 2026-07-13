


import uuid
from decimal import Decimal

from django.utils.text import slugify


def generate_sku(category_name, product_name):
    """
    Generate a unique SKU.

    Example:
    ELE-LAP-8A4F21
    """
    category = slugify(category_name)[:3].upper()
    product = slugify(product_name)[:3].upper()
    unique = uuid.uuid4().hex[:6].upper()

    return f"{category}-{product}-{unique}"


def generate_slug(name):
    """
    Generate a URL-friendly slug.
    """
    return slugify(name)


def calculate_discount_price(price, discount_percentage):
    """
    Calculate the discounted price.
    """
    if discount_percentage <= 0:
        return price

    discount = (
        Decimal(discount_percentage) / Decimal("100")
    ) * price

    return round(price - discount, 2)


def calculate_tax(price, tax_percentage=15):
    """
    Calculate tax amount.
    """
    tax = (
        Decimal(tax_percentage) / Decimal("100")
    ) * price

    return round(tax, 2)


def calculate_final_price(price, discount_percentage=0, tax_percentage=15):
    """
    Calculate the final selling price.
    """
    discounted = calculate_discount_price(
        price,
        discount_percentage,
    )

    tax = calculate_tax(
        discounted,
        tax_percentage,
    )

    return round(discounted + tax, 2)


def stock_status(stock):
    """
    Return a readable stock status.
    """
    if stock <= 0:
        return "Out of Stock"

    if stock <= 5:
        return "Low Stock"

    if stock <= 20:
        return "In Stock"

    return "Available"


def average_rating(reviews):
    """
    Calculate average review rating.
    """
    if not reviews.exists():
        return 0

    total = sum(
        review.rating
        for review in reviews
    )

    return round(
        total / reviews.count(),
        1,
    )


def rating_percentage(rating):
    """
    Convert rating to percentage.

    Example:
    4.5 → 90%
    """
    return round((rating / 5) * 100)


def is_new_product(product, days=30):
    """
    Determine whether a product is new.
    """
    from django.utils import timezone

    age = timezone.now() - product.created_at

    return age.days <= days


def product_badge(product):
    """
    Return a badge for product cards.
    """
    if product.stock <= 0:
        return "Sold Out"

    if is_new_product(product):
        return "New"

    return ""



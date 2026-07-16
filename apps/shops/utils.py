


from django.utils.text import slugify


def generate_shop_slug(name):
    """
    Generate a URL-friendly slug for a shop name.
    """

    return slugify(name)


def get_shop_display_name(shop):
    """
    Return the display name of a shop.
    """

    if shop.is_active:
        return shop.name

    return f"{shop.name} (Inactive)"


def is_shop_active(shop):
    """
    Check whether a shop is currently active.
    """

    return shop.is_active
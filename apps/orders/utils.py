


from datetime import datetime

from django.utils.crypto import get_random_string


def generate_order_number():
    """
    Generate a unique human-readable order number.
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    random_part = get_random_string(
        length=4,
        allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    )

    return f"ORD-{timestamp}-{random_part}"



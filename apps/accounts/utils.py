


"""
Utility functions for the accounts application.

These helpers are:
- Stateless
- Reusable
- Independent of business rules
"""

import secrets
import string


def generate_verification_code(length=6):
    """
    Generate a numeric verification code.

    Example:
        483920
    """
    digits = string.digits

    return "".join(
        secrets.choice(digits)
        for _ in range(length)
    )


def generate_random_token(length=32):
    """
    Generate a secure random token.

    Useful for:
    - Email verification
    - Password reset
    - API tokens (simple cases)
    """
    alphabet = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def mask_email(email):
    """
    Hide part of an email address.

    Example:

    john@example.com

    becomes

    jo***@example.com
    """

    if "@" not in email:
        return email

    username, domain = email.split("@")

    if len(username) <= 2:
        hidden = "*" * len(username)
    else:
        hidden = (
            username[:2]
            + "*" * (len(username) - 2)
        )

    return f"{hidden}@{domain}"



def get_client_ip(request):
    """
    Return the client's IP address.

    Supports proxies.
    """

    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.META.get(
        "REMOTE_ADDR"
    )


def normalize_email(email):
    """
    Normalize email addresses.

    Example:

    JOHN@Example.COM

    becomes

    john@example.com
    """

    return email.strip().lower()


def build_full_name(user):
    """
    Return a nicely formatted full name.
    """

    return (
        f"{user.first_name} {user.last_name}"
    ).strip()
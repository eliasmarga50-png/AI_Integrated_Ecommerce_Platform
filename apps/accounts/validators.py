


import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    """
    Validate a phone number.

    Accepts an optional '+' followed by 10–15 digits.
    Examples:
        +251912345678
        0912345678
    """

    pattern = r"^\+?\d{10,15}$"

    if not re.fullmatch(pattern, value):
        raise ValidationError(
            _(
                "Enter a valid phone number. "
                "It must contain only digits and may begin with '+'."
            )
        )


def validate_username(value):
    """
    Validate username format.
    """

    pattern = r"^[A-Za-z0-9_]{4,30}$"

    if not re.fullmatch(pattern, value):
        raise ValidationError(
            _(
                "Username must contain only letters, numbers, "
                "and underscores, and be between 4 and 30 characters."
            )
        )


def validate_name(value):
    """
    Validate person's first or last name.
    """

    if len(value.strip()) < 2:
        raise ValidationError(
            _("Name must contain at least two characters.")
        )

    if not value.replace(" ", "").isalpha():
        raise ValidationError(
            _("Name should contain letters only.")
        )

"""
Reusable permission helpers for the accounts app.
"""

from django.contrib.auth import get_user_model

User = get_user_model()


def is_authenticated(user):
    """
    Returns True if the user is authenticated.
    """
    return user.is_authenticated


def is_customer(user):
    """
    Returns True if the user is a customer.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.CUSTOMER
    )


def is_seller(user):
    """
    Returns True if the user is a seller.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.SELLER
    )


def is_admin(user):
    """
    Returns True if the user is an administrator.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.ADMIN
    )


def is_staff_member(user):
    """
    Returns True if the user can access
    Django administration.
    """
    return (
        user.is_authenticated
        and user.is_staff
    )


def is_superuser(user):
    """
    Returns True if the user is a superuser.
    """
    return (
        user.is_authenticated
        and user.is_superuser
    )
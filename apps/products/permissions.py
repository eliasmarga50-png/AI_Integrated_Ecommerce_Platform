


from django.core.exceptions import PermissionDenied


class ProductPermission:
    """
    Centralized permission checks for the Products app.

    Keeping permission logic in one place makes it easier
    to maintain and reuse across views, services, and APIs.
    """

    @staticmethod
    def is_authenticated(user):
        """
        Check whether the user is authenticated.
        """
        return user.is_authenticated

    @staticmethod
    def is_staff(user):
        """
        Check whether the user is a staff member.
        """
        return (
            user.is_authenticated and
            user.is_staff
        )

    @staticmethod
    def is_superuser(user):
        """
        Check whether the user is a superuser.
        """
        return (
            user.is_authenticated and
            user.is_superuser
        )

    @staticmethod
    def can_view_products(user):
        """
        Everyone can browse products.
        """
        return True

    @staticmethod
    def can_view_product_details(user):
        """
        Everyone can view product details.
        """
        return True

    @staticmethod
    def can_review_product(user):
        """
        Only logged-in users may submit reviews.
        """
        return user.is_authenticated

    @staticmethod
    def can_create_product(user):
        """
        Only staff members and superusers
        may create products.
        """
        return (
            user.is_authenticated and
            (
                user.is_staff or
                user.is_superuser
            )
        )

    @staticmethod
    def can_update_product(user):
        """
        Only staff members and superusers
        may update products.
        """
        return (
            user.is_authenticated and
            (
                user.is_staff or
                user.is_superuser
            )
        )

    @staticmethod
    def can_delete_product(user):
        """
        Only superusers may delete products.
        """
        return (
            user.is_authenticated and
            user.is_superuser
        )

    @staticmethod
    def can_manage_inventory(user):
        """
        Inventory management is restricted
        to staff and administrators.
        """
        return (
            user.is_authenticated and
            (
                user.is_staff or
                user.is_superuser
            )
        )

    @staticmethod
    def can_feature_product(user):
        """
        Only superusers can feature products.
        """
        return (
            user.is_authenticated and
            user.is_superuser
        )

    @staticmethod
    def require(permission):
        """
        Raise PermissionDenied if permission fails.
        """
        if not permission:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )
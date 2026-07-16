


from django.db import transaction

from .models import Shop


class ShopService:
    """
    Handles business logic related to shops.
    """

    @staticmethod
    @transaction.atomic
    def create_shop(
        *,
        owner,
        name,
        description="",
        logo=None,
    ):
        """
        Create a new shop for a user.
        """

        shop = Shop.objects.create(
            owner=owner,
            name=name,
            description=description,
            logo=logo,
        )

        return shop

    @staticmethod
    @transaction.atomic
    def update_shop(
        *,
        shop,
        name,
        description="",
        logo=None,
        is_active=True,
    ):
        """
        Update an existing shop.
        """

        shop.name = name
        shop.description = description
        shop.is_active = is_active

        if logo is not None:
            shop.logo = logo

        shop.save()

        return shop

    @staticmethod
    @transaction.atomic
    def deactivate_shop(*, shop):
        """
        Deactivate a shop without deleting it.
        """

        shop.is_active = False
        shop.save(update_fields=["is_active"])

        return shop

    @staticmethod
    @transaction.atomic
    def activate_shop(*, shop):
        """
        Activate a previously deactivated shop.
        """

        shop.is_active = True
        shop.save(update_fields=["is_active"])

        return shop
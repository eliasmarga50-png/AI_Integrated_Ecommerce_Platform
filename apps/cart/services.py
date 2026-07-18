


from django.db import transaction

from .models import Cart, CartItem


class CartService:
    """
    Business logic for cart operations.
    """

    @staticmethod
    def get_or_create_cart(user):
        """
        Return the user's cart.
        Create it if it does not exist.
        """

        cart, _ = Cart.objects.get_or_create(
            owner=user
        )

        return cart

    @staticmethod
    @transaction.atomic
    def add_product(cart, product, quantity=1):
        """
        Add a product to the cart.

        If the product already exists in the cart,
        increase its quantity.
        """

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity,
            },
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

        return cart_item

    @staticmethod
    @transaction.atomic
    def update_quantity(cart, product, quantity):
        """
        Update the quantity of a product in the cart.
        """

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        cart_item = CartItem.objects.get(
            cart=cart,
            product=product,
        )

        cart_item.quantity = quantity

        cart_item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

        return cart_item

    @staticmethod
    @transaction.atomic
    def remove_product(cart, product):
        """
        Remove a product from the cart.
        """

        deleted_count, _ = CartItem.objects.filter(
            cart=cart,
            product=product,
        ).delete()

        return deleted_count > 0

    @staticmethod
    @transaction.atomic
    def clear_cart(cart):
        """
        Remove all products from the cart.
        """

        CartItem.objects.filter(
            cart=cart
        ).delete()

    @staticmethod
    def get_cart_items(cart):
        """
        Return all items belonging to the cart.
        """

        return cart.items.select_related(
            "product"
        ).all()

    @staticmethod
    def get_cart_summary(cart):
        """
        Return a summary of the cart.
        """

        return {
            "cart": cart,
            "items": CartService.get_cart_items(cart),
            "total_items": cart.total_items,
            "total_price": cart.total_price,
        }
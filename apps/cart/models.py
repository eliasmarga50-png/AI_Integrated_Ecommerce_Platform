


from django.conf import settings
from django.db import models

from apps.products.models import Product


class Cart(models.Model):
    """
    Represents a shopping cart owned by a user.
    """

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.owner.username}'s Cart"

    @property
    def total_items(self):
        """
        Return the total quantity of products in the cart.
        """

        return sum(
            item.quantity
            for item in self.items.all()
        )

    @property
    def total_price(self):
        """
        Return the total price of all cart items.
        """

        return sum(
            item.subtotal
            for item in self.items.all()
        )


class CartItem(models.Model):
    """
    Represents a product inside a shopping cart.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-added_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart",
            )
        ]

    def __str__(self):
        return (
            f"{self.product.name} "
            f"x {self.quantity}"
        )

    @property
    def subtotal(self):
        """
        Return the total price for this cart item.
        """

        return self.product.price * self.quantity



from decimal import Decimal

from django.db import transaction

from .models import Order, OrderItem
from .utils import generate_order_number


class OrderService:
    """
    Contains business logic related to Orders.
    """

    @staticmethod
    def calculate_order_total(cart):
        """
        Calculate the total price of all items in a cart.
        """

        total = Decimal("0.00")

        for cart_item in cart.items.select_related("product"):
            total += (
                cart_item.product.price
                * cart_item.quantity
            )

        return total

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(
        cart,
        shipping_address,
        shipping_city,
        shipping_phone,
    ):
        """
        Create an Order and its OrderItems from a Cart.
        """

        order = Order.objects.create(
            user=cart.user,
            order_number=generate_order_number(),
            total_amount=Decimal("0.00"),
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_phone=shipping_phone,
        )

        total_amount = Decimal("0.00")

        cart_items = cart.items.select_related("product")

        for cart_item in cart_items:
            product = cart_item.product

            subtotal = (
                product.price
                * cart_item.quantity
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=cart_item.quantity,
                subtotal=subtotal,
            )

            total_amount += subtotal

        order.total_amount = total_amount
        order.save(
            update_fields=["total_amount"],
        )

        return order

    @staticmethod
    def get_user_orders(user):
        """
        Return all orders belonging to a specific user.
        """

        return (
            Order.objects
            .filter(user=user)
            .prefetch_related("items")
        )

    @staticmethod
    def get_order(order_number, user):
        """
        Return a specific order belonging to a specific user.
        """

        return (
            Order.objects
            .prefetch_related("items")
            .get(
                order_number=order_number,
                user=user,
            )
        )
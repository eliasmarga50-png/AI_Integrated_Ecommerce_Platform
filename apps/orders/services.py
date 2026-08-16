


from decimal import Decimal

from django.db import transaction

from apps.products.models import Product

from .exceptions import (
    EmptyCartError,
    InsufficientStockError,
    ProductUnavailableError,
)
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

        Inventory is validated and reserved atomically so that
        concurrent checkouts cannot oversell available stock.
        """

        cart_items = list(
            cart.items.select_related("product")
        )

        if not cart_items:
            raise EmptyCartError(
                "Cannot create an order from an empty cart."
            )

        product_ids = [
            cart_item.product_id
            for cart_item in cart_items
        ]

        locked_products = {
            product.id: product
            for product in (
                Product.objects
                .select_for_update()
                .filter(id__in=product_ids)
            )
        }

        total_amount = Decimal("0.00")

        for cart_item in cart_items:
            product = locked_products.get(
                cart_item.product_id
            )

            if product is None:
                raise ProductUnavailableError(
                    "One or more products are no longer available."
                )

            if not product.is_available:
                raise ProductUnavailableError(
                    f"{product.name} is no longer available."
                )

            if cart_item.quantity > product.stock:
                raise InsufficientStockError(
                    f"Insufficient stock for {product.name}."
                )

        order = Order.objects.create(
            user=cart.owner,
            order_number=generate_order_number(),
            total_amount=Decimal("0.00"),
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_phone=shipping_phone,
        )

        for cart_item in cart_items:
            product = locked_products[
                cart_item.product_id
            ]

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

            product.stock -= cart_item.quantity
            
            if product.stock==0:
            	product.is_available=False
            	
            product.save(
                update_fields=[
                    "stock",
                    "is_available",
                    "updated_at",
                ]
            )

            total_amount += subtotal

        order.total_amount = total_amount
        order.save(
            update_fields=[
                "total_amount",
                "updated_at",
            ],
        )
        
        cart.items.all().delete()

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




from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Displays order items directly inside the Order admin page.
    """

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product_name",
        "unit_price",
        "subtotal",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order.
    """

    list_display = (
        "order_number",
        "user",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "order_number",
        "total_amount",
        "created_at",
        "updated_at",
    )

    inlines = (
        OrderItemInline,
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrderItem.
    """

    list_display = (
        "product_name",
        "order",
        "unit_price",
        "quantity",
        "subtotal",
    )

    search_fields = (
        "product_name",
        "order__order_number",
    )

    readonly_fields = (
        "product_name",
        "unit_price",
        "subtotal",
    )

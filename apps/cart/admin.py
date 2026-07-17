


from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """
    Display cart items inside the Cart admin page.
    """

    model = CartItem

    extra = 0

    readonly_fields = (
        "subtotal",
        "added_at",
        "updated_at",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin configuration for Cart.
    """

    list_display = (
        "owner",
        "total_items",
        "total_price",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "owner__username",
        "owner__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "total_items",
        "total_price",
    )

    inlines = [
        CartItemInline,
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for CartItem.
    """

    list_display = (
        "cart",
        "product",
        "quantity",
        "subtotal",
        "added_at",
    )

    list_filter = (
        "added_at",
        "updated_at",
    )

    search_fields = (
        "cart__owner__username",
        "cart__owner__email",
        "product__name",
    )

    readonly_fields = (
        "subtotal",
        "added_at",
        "updated_at",
    )



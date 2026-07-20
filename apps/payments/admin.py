


from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "user",
        "amount",
        "currency",
        "status",
        "gateway",
        "payment_method",
        "created_at",
    )

    list_filter = (
        "status",
        "gateway",
        "payment_method",
        "currency",
        "created_at",
    )

    search_fields = (
        "transaction_reference",
        "user__username",
        "user__email",
        "order__id",
    )

    readonly_fields = (
        "user",
        "order",
        "amount",
        "currency",
        "status",
        "gateway",
        "payment_method",
        "transaction_reference",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"



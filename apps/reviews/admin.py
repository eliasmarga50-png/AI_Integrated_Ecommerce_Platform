


from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "is_edited",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_edited",
        "created_at",
    )

    search_fields = (
        "title",
        "comment",
        "user__username",
        "product__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    fieldsets = (
        (
            "Review Information",
            {
                "fields": (
                    "product",
                    "user",
                    "rating",
                    "title",
                    "comment",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "is_edited",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    
    
    



from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render


def home(request):
    return render(
        request,
        "public/home.html",
    )


urlpatterns = [
    # ========================================================
    # ADMIN
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ========================================================
    # ACCOUNTS
    # ========================================================

    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),

    # ========================================================
    # PRODUCTS
    # ========================================================

    path(
        "products/",
        include("apps.products.urls"),
    ),

    # ========================================================
    # SHOPS
    # ========================================================

    path(
        "shops/",
        include("apps.shops.urls"),
    ),

    # ========================================================
    # CART
    # ========================================================

    path(
        "cart/",
        include("apps.cart.urls"),
    ),

    # ========================================================
    # ORDERS
    # ========================================================

    path(
        "orders/",
        include("apps.orders.urls"),
    ),

    # ========================================================
    # PAYMENTS
    # ========================================================

    path(
        "payments/",
        include("apps.payments.urls"),
    ),

    # ========================================================
    # REVIEWS
    # ========================================================

    path(
        "reviews/",
        include("apps.reviews.urls"),
    ),

    # ========================================================
    # AI
    # ========================================================

    path(
        "ai/",
        include("apps.ai.urls"),
    ),

    # ========================================================
    # HOME
    # ========================================================

    path(
        "",
        home,
        name="home",
    ),
]


# ============================================================
# DEVELOPMENT MEDIA SERVING
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
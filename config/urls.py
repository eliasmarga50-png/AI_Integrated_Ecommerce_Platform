

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

from apps.products.models import Product, Category
from apps.shops.models import Shop


# ========================================================
# VIEWS
# ========================================================

def home(request):
    """
    Renders the public homepage with featured products, 
    categories, and active shops.
    """
    products = (
        Product.objects
        .filter(is_available=True)
        .select_related("category", "shop")
        .order_by("-created_at")[:8]
    )

    categories = Category.objects.all()[:8]

    shops = (
        Shop.objects
        .filter(is_active=True)
        .select_related("owner")
        .order_by("-created_at")[:6]
    )

    return render(
        request,
        "public/home.html",
        {
            "featured_products": products,
            "categories": categories,
            "featured_shops": shops,
        },
    )


# ========================================================
# URL CONFIGURATION
# ========================================================

urlpatterns = [
    # ADMIN
    path(
        "admin/",
        admin.site.urls,
    ),

    # ACCOUNTS
    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),

    # PRODUCTS
    path(
        "products/",
        include("apps.products.urls"),
    ),

    # SHOPS
    path(
        "shops/",
        include("apps.shops.urls"),
    ),

    # CART
    path(
        "cart/",
        include("apps.cart.urls"),
    ),

    # ORDERS
    path(
        "orders/",
        include("apps.orders.urls"),
    ),

    # PAYMENTS
    path(
        "payments/",
        include("apps.payments.urls"),
    ),

    # REVIEWS
    path(
        "reviews/",
        include("apps.reviews.urls"),
    ),
    
    # DASHBOARD
    path(
        "dashboard/",
        include("apps.dashboard.urls"),
    ),

    # AI
    path(
        "ai/",
        include("apps.ai.urls"),
    ),

    # HOME
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

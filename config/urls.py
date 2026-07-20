


from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return HttpResponse(
        """
        <h1>Welcome to AI Ecommerce</h1>
        <p>Our store is coming soon.</p>
        """
    )


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "accounts/",
        include(
            "apps.accounts.urls"
        ),
    ),

    path(
        "products/",
        include(
            "apps.products.urls"
        ),
    ),

    path(
        "",
        home,
        name="home",
    ),
    
    path(
      "shops/",
      include("apps.shops.urls")
    ),
    
    path(
      "cart/",
      include("apps.cart.urls")
    ),
    
    path(
    "orders/",
    include("apps.orders.urls")
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
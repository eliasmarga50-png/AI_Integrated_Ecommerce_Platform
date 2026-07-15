


from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse


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
]
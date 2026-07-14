


from django.urls import path

from .views import (
    CategoryProductListView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

app_name = "products"

urlpatterns = [
    # Product list
    path(
        "",
        ProductListView.as_view(),
        name="list",
    ),

    # Create must come BEFORE slug routes
    path(
        "create/",
        ProductCreateView.as_view(),
        name="create",
    ),

    # Category
    path(
        "category/<slug:slug>/",
        CategoryProductListView.as_view(),
        name="category",
    ),

    # Update
    path(
        "<slug:slug>/update/",
        ProductUpdateView.as_view(),
        name="update",
    ),

    # Delete
    path(
        "<slug:slug>/delete/",
        ProductDeleteView.as_view(),
        name="delete",
    ),

    # Detail should be LAST
    path(
        "<slug:slug>/",
        ProductDetailView.as_view(),
        name="detail",
    ),
]
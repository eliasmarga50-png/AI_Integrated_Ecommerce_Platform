


from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path(
        "",
        views.product_list,
        name="product_list",
    ),
    path(
        "<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path(
        "category/<slug:slug>/",
        views.category_products,
        name="category_products",
    ),
    path(
        "create/",
        views.create_product,
        name="create_product",
    ),
    path(
        "update/<slug:slug>/",
        views.update_product,
        name="update_product",
    ),
    path(
        "delete/<slug:slug>/",
        views.delete_product,
        name="delete_product",
    ),
]



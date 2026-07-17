


from django.urls import path

from . import views


app_name = "shops"


urlpatterns = [
    path(
        "",
        views.shop_list,
        name="shop_list",
    ),

    path(
        "create/",
        views.shop_create,
        name="shop_create",
    ),

    path(
        "<slug:slug>/",
        views.shop_detail,
        name="shop_detail",
    ),

    path(
        "<slug:slug>/update/",
        views.shop_update,
        name="shop_update",
    ),

    path(
        "<slug:slug>/deactivate/",
        views.shop_deactivate,
        name="shop_deactivate",
    ),
]
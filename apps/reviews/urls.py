


from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path(
        "products/<int:product_id>/reviews/",
        views.review_list,
        name="review_list",
    ),
    path(
        "products/<int:product_id>/reviews/create/",
        views.create_review,
        name="create_review",
    ),
    path(
        "reviews/<int:pk>/",
        views.review_detail,
        name="review_detail",
    ),
    path(
        "reviews/<int:pk>/edit/",
        views.update_review,
        name="update_review",
    ),
    path(
        "reviews/<int:pk>/delete/",
        views.delete_review,
        name="delete_review",
    ),
]



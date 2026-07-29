


from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.reviews import views


class ReviewURLTests(SimpleTestCase):
    """
    Tests for review URL routing.
    """

    # --------------------------------------------------
    # Review List
    # --------------------------------------------------

    def test_review_list_url(self):
        url = reverse("reviews:review_list", kwargs={"product_id": 1})

        self.assertEqual(
            resolve(url).func.__name__,
            "ReviewListView" if hasattr(views.ReviewListView, "as_view") else "review_list",
        )

    # --------------------------------------------------
    # Review Detail
    # --------------------------------------------------

    def test_review_detail_url(self):
        url = reverse(
            "reviews:review_detail",
            args=[1],
        )

        self.assertEqual(
            resolve(url).func.__name__,
            "ReviewDetailView" if hasattr(views.ReviewDetailView, "as_view") else "review_detail",
        )

    # --------------------------------------------------
    # Review Create
    # --------------------------------------------------

    def test_review_create_url(self):
        url = reverse(
            "reviews:review_create",
            args=[1],
        )

        self.assertEqual(
            resolve(url).func.__name__,
            "ReviewCreateView" if hasattr(views.ReviewCreateView, "as_view") else "review_create",
        )

    # --------------------------------------------------
    # Review Update
    # --------------------------------------------------

    def test_review_update_url(self):
        url = reverse(
            "reviews:review_update",
            args=[1],
        )

        self.assertEqual(
            resolve(url).func.__name__,
            "ReviewUpdateView" if hasattr(views.ReviewUpdateView, "as_view") else "review_update",
        )

    # --------------------------------------------------
    # Review Delete
    # --------------------------------------------------

    def test_review_delete_url(self):
        url = reverse(
            "reviews:review_delete",
            args=[1],
        )

        self.assertEqual(
            resolve(url).func.__name__,
            "ReviewDeleteView" if hasattr(views.ReviewDeleteView, "as_view") else "review_delete",
        )



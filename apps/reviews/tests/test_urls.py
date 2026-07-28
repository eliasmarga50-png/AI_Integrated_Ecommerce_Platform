


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
        url = reverse("reviews:review_list")

        self.assertEqual(
            resolve(url).func.view_class,
            views.ReviewListView,
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
            resolve(url).func.view_class,
            views.ReviewDetailView,
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
            resolve(url).func.view_class,
            views.ReviewCreateView,
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
            resolve(url).func.view_class,
            views.ReviewUpdateView,
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
            resolve(url).func.view_class,
            views.ReviewDeleteView,
        )



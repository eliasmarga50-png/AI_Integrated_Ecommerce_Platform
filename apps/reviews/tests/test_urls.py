


from django.test import SimpleTestCase
from django.urls import resolve, reverse


class ReviewURLTests(SimpleTestCase):
    """
    Tests for review URL routing.
    """

    # --------------------------------------------------
    # Review List
    # --------------------------------------------------

    def test_review_list_url(self):
        url = reverse("reviews:review_list", kwargs={"product_id": 1})
        self.assertEqual(resolve(url).func.__name__, "review_list")

    # --------------------------------------------------
    # Review Detail
    # --------------------------------------------------

    def test_review_detail_url(self):
        url = reverse("reviews:review_detail", args=[1])
        self.assertEqual(resolve(url).func.__name__, "review_detail")

    # --------------------------------------------------
    # Review Create
    # --------------------------------------------------

    def test_review_create_url(self):
        url = reverse("reviews:review_create", args=[1])
        self.assertEqual(resolve(url).func.__name__, "create_review")

    # --------------------------------------------------
    # Review Update
    # --------------------------------------------------

    def test_review_update_url(self):
        url = reverse("reviews:review_update", args=[1])
        self.assertEqual(resolve(url).func.__name__, "update_review")

    # --------------------------------------------------
    # Review Delete
    # --------------------------------------------------

    def test_review_delete_url(self):
        url = reverse("reviews:review_delete", args=[1])
        self.assertEqual(resolve(url).func.__name__, "delete_review")



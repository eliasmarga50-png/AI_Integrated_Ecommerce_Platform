


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.products.models import Category, Product
from apps.reviews.models import Review


User = get_user_model()


class ReviewViewsTests(TestCase):
    """
    Integration tests for review views.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
        )

        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            slug="laptop",
            description="Gaming Laptop",
            price=Decimal("1500.00"),
            stock=10,
        )

        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Amazing product!",
        )

    # --------------------------------------------------
    # Review List
    # --------------------------------------------------

    def test_review_list_page(self):
        response = self.client.get(reverse("reviews:review_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reviews/review_list.html",
        )

    # --------------------------------------------------
    # Review Detail
    # --------------------------------------------------

    def test_review_detail_page(self):
        response = self.client.get(
            reverse(
                "reviews:review_detail",
                args=[self.review.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reviews/review_detail.html",
        )

    # --------------------------------------------------
    # Create Review
    # --------------------------------------------------

    def test_login_required_for_create(self):
        response = self.client.get(
            reverse(
                "reviews:review_create",
                args=[self.product.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_create_review(self):
        self.client.login(
            username="elias",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "reviews:review_create",
                args=[self.product.pk],
            ),
            {
                "rating": 4,
                "title": "Very Good",
                "comment": "Nice laptop.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

    # --------------------------------------------------
    # Update Review
    # --------------------------------------------------

    def test_owner_can_update_review(self):
        self.client.login(
            username="elias",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "reviews:review_update",
                args=[self.review.pk],
            ),
            {
                "rating": 3,
                "title": "Updated",
                "comment": "Changed opinion.",
            },
        )

        self.review.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(
            self.review.title,
            "Updated",
        )

    def test_non_owner_cannot_update_review(self):
        self.client.login(
            username="john",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "reviews:review_update",
                args=[self.review.pk],
            ),
            {
                "rating": 1,
                "title": "Hack",
                "comment": "Should fail",
            },
        )

        self.assertIn(response.status_code, [403, 404])

    # --------------------------------------------------
    # Delete Review
    # --------------------------------------------------

    def test_owner_can_delete_review(self):
        self.client.login(
            username="elias",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "reviews:review_delete",
                args=[self.review.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Review.objects.count(),
            0,
        )

    def test_non_owner_cannot_delete_review(self):
        self.client.login(
            username="john",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "reviews:review_delete",
                args=[self.review.pk],
            )
        )

        self.assertIn(response.status_code, [403, 404])

    # --------------------------------------------------
    # Invalid Form
    # --------------------------------------------------

    def test_create_review_invalid_data(self):
        self.client.login(
            username="elias",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "reviews:review_create",
                args=[self.product.pk],
            ),
            {
                "rating": 10,
                "title": "",
                "comment": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "title", "This field is required.")

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    def test_review_in_context(self):
        response = self.client.get(
            reverse(
                "reviews:review_detail",
                args=[self.review.pk],
            )
        )

        self.assertEqual(
            response.context["review"],
            self.review,
        )



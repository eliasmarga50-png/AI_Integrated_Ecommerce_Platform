


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import Category, Product
from apps.reviews.forms import ReviewForm


User = get_user_model()


class ReviewFormTests(TestCase):
    """
    Tests for the ReviewForm.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
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

    # -----------------------------------------------------
    # Valid Form
    # -----------------------------------------------------

    def test_valid_form(self):
        form = ReviewForm(data={
            "rating": 5,
            "title": "Excellent",
            "comment": "Fantastic laptop!",
        })

        self.assertTrue(form.is_valid())

    # -----------------------------------------------------
    # Rating Validation
    # -----------------------------------------------------

    def test_rating_required(self):
        form = ReviewForm(data={
            "title": "Good",
            "comment": "Nice",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_too_low(self):
        form = ReviewForm(data={
            "rating": 0,
            "title": "Bad",
            "comment": "Invalid",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_too_high(self):
        form = ReviewForm(data={
            "rating": 6,
            "title": "Bad",
            "comment": "Invalid",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    # -----------------------------------------------------
    # Title Validation
    # -----------------------------------------------------

    def test_title_required(self):
        form = ReviewForm(data={
            "rating": 5,
            "title": "",
            "comment": "Nice",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    # -----------------------------------------------------
    # Comment Validation
    # -----------------------------------------------------

    def test_comment_required(self):
        form = ReviewForm(data={
            "rating": 5,
            "title": "Excellent",
            "comment": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("comment", form.errors)

    # -----------------------------------------------------
    # Cleaned Data
    # -----------------------------------------------------

    def test_cleaned_data(self):
        form = ReviewForm(data={
            "rating": 4,
            "title": "Very Good",
            "comment": "Works perfectly.",
        })

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["rating"], 4)
        self.assertEqual(form.cleaned_data["title"], "Very Good")
        self.assertEqual(
            form.cleaned_data["comment"],
            "Works perfectly."
        )

    # -----------------------------------------------------
    # Long Comment
    # -----------------------------------------------------

    def test_long_comment(self):
        form = ReviewForm(data={
            "rating": 5,
            "title": "Excellent",
            "comment": "A" * 500,
        })

        self.assertTrue(form.is_valid())

    # -----------------------------------------------------
    # Whitespace Handling
    # -----------------------------------------------------

    def test_title_is_stripped(self):
        form = ReviewForm(data={
            "rating": 5,
            "title": "   Amazing Product   ",
            "comment": "Nice",
        })

        self.assertTrue(form.is_valid())

        self.assertEqual(
            form.cleaned_data["title"],
            "Amazing Product",
        )

    def test_comment_is_stripped(self):
        form = ReviewForm(data={
            "rating": 5,
            "title": "Excellent",
            "comment": "   Great product!   ",
        })

        self.assertTrue(form.is_valid())

        self.assertEqual(
            form.cleaned_data["comment"],
            "Great product!",
        )



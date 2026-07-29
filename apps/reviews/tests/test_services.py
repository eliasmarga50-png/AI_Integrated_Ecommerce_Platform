


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.products.models import Category, Product
from apps.reviews.models import Review
from apps.reviews.services import ReviewService


User = get_user_model()


class ReviewServiceTests(TestCase):
    """
    Tests for the ReviewService.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="password123",
        )

        self.second_user = User.objects.create_user(
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
            stock=5,
        )

    # --------------------------------------------------
    # Create Review
    # --------------------------------------------------

    def test_create_review(self):
        review = ReviewService.create_review(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Fantastic laptop!",
        )

        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)

    def test_create_review_invalid_rating(self):
        """Should raise ValidationError if rating is out of bounds."""
        with self.assertRaises(ValidationError):
            ReviewService.create_review(
                user=self.user,
                product=self.product,
                rating=6,  # Invalid
                title="Bad Rating",
                comment="Testing bounds",
            )

    def test_create_review_duplicate_prevention(self):
        """Should raise ValidationError on duplicate product reviews by same user."""
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            title="First Review",
            comment="Nice",
        )

        with self.assertRaises(ValidationError):
            ReviewService.create_review(
                user=self.user,
                product=self.product,
                rating=5,
                title="Second Review",
                comment="Trying to review again",
            )

    # --------------------------------------------------
    # Update Review
    # --------------------------------------------------

    def test_update_review(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            title="Average",
            comment="Okay",
        )

        # FIX: Passed review.id as review_id to match service signature
        updated = ReviewService.update_review(
            review.id,
            rating=5,
            title="Excellent",
            comment="Changed my mind.",
        )

        self.assertEqual(updated.rating, 5)
        self.assertEqual(updated.title, "Excellent")
        self.assertEqual(updated.comment, "Changed my mind.")
        self.assertTrue(updated.is_edited)

    def test_update_review_invalid_rating(self):
        """Should raise ValidationError if updated rating is out of bounds."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            title="Average",
            comment="Okay",
        )

        with self.assertRaises(ValidationError):
            ReviewService.update_review(
                review.id,
                rating=0,  # Invalid
                title="Updated Title",
                comment="Updated comment",
            )

    # --------------------------------------------------
    # Delete Review
    # --------------------------------------------------

    def test_delete_review(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            title="Good",
            comment="Nice",
        )

        # FIX: Passed review.id instead of the model object instance
        deleted = ReviewService.delete_review(review.id)

        self.assertTrue(deleted)
        self.assertEqual(Review.objects.count(), 0)

    # --------------------------------------------------
    # Average Rating
    # --------------------------------------------------

    def test_average_rating(self):
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Perfect",
        )

        Review.objects.create(
            user=self.second_user,
            product=self.product,
            rating=3,
            title="Average",
            comment="Okay",
        )

        average = ReviewService.get_average_rating(self.product)

        self.assertEqual(average, 4.0)

    # --------------------------------------------------
    # Review Count
    # --------------------------------------------------

    def test_review_count(self):
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Perfect",
        )

        Review.objects.create(
            user=self.second_user,
            product=self.product,
            rating=4,
            title="Good",
            comment="Nice",
        )

        count = ReviewService.get_review_count(self.product)

        self.assertEqual(count, 2)

    # --------------------------------------------------
    # User Review Lookup
    # --------------------------------------------------

    def test_get_user_review(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Perfect",
        )

        found = ReviewService.get_user_review(
            self.user,
            self.product,
        )

        self.assertEqual(found, review)

    # --------------------------------------------------
    # Duplicate Review Prevention
    # --------------------------------------------------

    def test_user_has_reviewed(self):
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title="Excellent",
            comment="Perfect",
        )

        self.assertTrue(
            ReviewService.user_has_reviewed(
                self.user,
                self.product,
            )
        )

    def test_user_has_not_reviewed(self):
        self.assertFalse(
            ReviewService.user_has_reviewed(
                self.user,
                self.product,
            )
        )

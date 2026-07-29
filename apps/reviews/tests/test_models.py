


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.products.models import Category, Product
from apps.reviews.models import Review


User = get_user_model()


class ReviewModelTests(TestCase):
    """
    Tests for the Review model.
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
            description="Gaming laptop",
            price=Decimal("1500.00"),
            stock=10,
        )

        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Amazing Product",
            comment="Worth every penny!",
        )

    # -----------------------------------------------------
    # Creation
    # -----------------------------------------------------

    def test_review_creation(self):
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.title, "Amazing Product")
        self.assertEqual(self.review.comment, "Worth every penny!")

    # -----------------------------------------------------
    # String Representation
    # -----------------------------------------------------

    def test_string_representation(self):
        expected = f"{self.user} - {self.product} (5★)"
        self.assertEqual(str(self.review), expected)

    # -----------------------------------------------------
    # Timestamps
    # -----------------------------------------------------

    def test_created_at_is_set(self):
        self.assertIsNotNone(self.review.created_at)

    def test_updated_at_is_set(self):
        self.assertIsNotNone(self.review.updated_at)

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    def test_rating_cannot_be_less_than_one(self):
        review = Review(
            product=self.product,
            user=self.user,
            rating=0,
            title="Bad",
            comment="Invalid rating",
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_cannot_be_greater_than_five(self):
        review = Review(
            product=self.product,
            user=self.user,
            rating=6,
            title="Too High",
            comment="Invalid rating",
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_valid_rating_passes_validation(self):
        other_user = User.objects.create_user(
            username="validation_user",
            email="val@example.com",
            password="password123",
        )
        review = Review(
            product=self.product,
            user=other_user,
            rating=4,
            title="Nice",
            comment="Good",
        )

        review.full_clean()

    # -----------------------------------------------------
    # Relationships
    # -----------------------------------------------------

    def test_review_belongs_to_product(self):
        self.assertEqual(self.review.product.name, "Laptop")

    def test_review_belongs_to_user(self):
        self.assertEqual(self.review.user.username, "elias")

    # -----------------------------------------------------
    # Cascade Delete
    # -----------------------------------------------------

    def test_deleting_product_deletes_review(self):
        self.product.delete()

        self.assertEqual(Review.objects.count(), 0)

    def test_deleting_user_deletes_review(self):
        self.user.delete()

        self.assertEqual(Review.objects.count(), 0)

    # -----------------------------------------------------
    # Ordering
    # -----------------------------------------------------

    def test_default_ordering(self):
        newer = Review.objects.create(
            product=self.product,
            user=User.objects.create_user(
                username="john",
                email="john@example.com",
                password="password123",
            ),
            rating=4,
            title="Good",
            comment="Nice",
        )

        reviews = list(Review.objects.all())

        self.assertEqual(reviews[0], newer)
        self.assertEqual(reviews[1], self.review)





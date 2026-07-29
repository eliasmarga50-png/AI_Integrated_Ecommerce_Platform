

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Avg

from .models import Review


class ReviewService:
    """
    Business logic for creating, updating,
    deleting and retrieving reviews.
    """

    @staticmethod
    @transaction.atomic
    def create_review(
        *,
        user,
        product,
        rating,
        title,
        comment,
    ):
        # Prevent runtime issues with invalid rating bounds
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")
            
        try:
            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                title=title,
                comment=comment,
            )
            # Optional: Hook to update product.average_rating here
            return review
        except IntegrityError:
            raise ValidationError("You have already reviewed this product.")

    @staticmethod
    @transaction.atomic
    def update_review(
        review_id,  # Passing ID ensures we can lock the row fresh
        *,
        rating,
        title,
        comment,
    ):
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")

        # select_for_update() prevents concurrent modification bugs
        review = (
            Review.objects
            .select_for_update()
            .get(pk=review_id)
        )
        
        review.rating = rating
        review.title = title
        review.comment = comment
        review.is_edited = True
        review.save()

        # Optional: Hook to update product.average_rating here
        return review

    @staticmethod
    @transaction.atomic
    def delete_review(review_id):
        # Using ID and direct queryset delete is faster and avoids memory overhead
        count, _ = Review.objects.filter(pk=review_id).delete()
        # Optional: Hook to update product.average_rating here
        return count > 0

    @staticmethod
    def get_product_reviews(product):
        return (
            Review.objects
            .filter(product=product)
            .select_related("user")
            .order_by("-created_at")  # Good practice to guarantee ordering
        )

    @staticmethod
    def calculate_average_rating(product):
        result = (
            Review.objects
            .filter(product=product)
            .aggregate(
                average=Avg("rating")
            )
        )
        
        return round(result["average"] or 0.0, 2)
    
    @staticmethod
    def get_average_rating(product):
        return ReviewService.calculate_average_rating(product)

    @staticmethod
    def get_review_count(product):
        return Review.objects.filter(
            product=product
        ).count()

    @staticmethod
    def get_user_review(user, product):
        return (
            Review.objects
            .filter(
                user=user,
                product=product,
            )
            .first()
        )

    @staticmethod
    def user_has_reviewed(user, product):
        return Review.objects.filter(
            user=user,
            product=product,
        ).exists()

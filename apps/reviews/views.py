


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from apps.products.models import Product

from .forms import ReviewForm
from .models import Review
from .services import ReviewService


def review_list(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
        "reviews": ReviewService.get_product_reviews(product),
        "average_rating": ReviewService.calculate_average_rating(product),
    }

    return render(request, "reviews/review_list.html", context)


def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    return render(
        request,
        "reviews/review_detail.html",
        {"review": review},
    )


@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            if ReviewService.user_has_reviewed(
               request.user,
               product,
            ):
            	form.add_error(
              	  None,
              	  "You have already reviewed this product.",
            	)
            	
            	return render(
            	   request,
            	   "reviews/review_form.html",
            	   {
            	      "form": form,
            	      "product": product,
            	   },
            	)
            ReviewService.create_review(
                user=request.user,
                product=product,
                rating=form.cleaned_data["rating"],
                title=form.cleaned_data["title"],
                comment=form.cleaned_data["comment"],
            )

            messages.success(
                request,
                "Your review has been submitted successfully.",
            )

            return redirect(
                "reviews:review_list",
                product_id=product.id,
            )
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "product": product,
        },
    )


@login_required
def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            # FIX: Passed review.id instead of the model instance object
            ReviewService.update_review(
                review.id,
                rating=form.cleaned_data["rating"],
                title=form.cleaned_data["title"],
                comment=form.cleaned_data["comment"],
            )

            messages.success(
                request,
                "Review updated successfully.",
            )

            return redirect(
                "reviews:review_detail",
                pk=review.pk,
            )
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "review": review,
        },
    )


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden()

    product_id = review.product.id

    if request.method == "POST":
        # FIX: Passed review.id instead of the model instance object
        ReviewService.delete_review(review.id)

        messages.success(
            request,
            "Review deleted successfully.",
        )

        return redirect(
            "reviews:review_list",
            product_id=product_id,
        )

    return render(
        request,
        "reviews/review_confirm_delete.html",
        {
            "review": review,
        },
    )
    
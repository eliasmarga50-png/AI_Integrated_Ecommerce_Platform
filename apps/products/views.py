


from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, ProductReviewForm
from .models import Category, Product


def product_list(request):
    """
    Display all available products.
    """
    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    context = {
        "products": products,
    }

    return render(
        request,
        "products/product_list.html",
        context,
    )


def product_detail(request, slug):
    """
    Display a single product and its reviews.
    """
    product = get_object_or_404(
        Product.objects.prefetch_related(
            "images",
            "reviews",
        ),
        slug=slug,
        is_available=True,
    )

    review_form = ProductReviewForm()

    context = {
        "product": product,
        "review_form": review_form,
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )


def category_products(request, slug):
    """
    Display products belonging to one category.
    """
    category = get_object_or_404(
        Category,
        slug=slug,
    )

    products = category.products.filter(
        is_available=True
    )

    context = {
        "category": category,
        "products": products,
    }

    return render(
        request,
        "products/category_products.html",
        context,
    )


def create_product(request):
    """
    Create a new product.
    """
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("products:product_list")

    else:
        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {"form": form},
    )


def update_product(request, slug):
    """
    Update an existing product.
    """
    product = get_object_or_404(
        Product,
        slug=slug,
    )

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            instance=product,
        )

        if form.is_valid():
            form.save()
            return redirect(
                "products:product_detail",
                slug=product.slug,
            )

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
            "product": product,
        },
    )


def delete_product(request, slug):
    """
    Delete a product.
    """
    product = get_object_or_404(
        Product,
        slug=slug,
    )

    if request.method == "POST":
        product.delete()
        return redirect("products:product_list")

    return render(
        request,
        "products/product_confirm_delete.html",
        {
            "product": product,
        },
    )
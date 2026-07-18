


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.products.models import Product

from .services import CartService


@login_required
def cart_detail(request):
    """
    Display the current user's cart.
    """

    cart = CartService.get_or_create_cart(
        user=request.user
    )

    summary = CartService.get_cart_summary(
        cart=cart
    )

    return render(
        request,
        "cart/cart_detail.html",
        summary,
    )


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the user's cart.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    cart = CartService.get_or_create_cart(
        user=request.user
    )

    quantity = int(
        request.POST.get(
            "quantity",
            1,
        )
    )

    CartService.add_product(
        cart=cart,
        product=product,
        quantity=quantity,
    )

    return redirect(
        "cart:cart_detail"
    )


@login_required
def update_cart_item(request, product_id):
    """
    Update the quantity of a product in the cart.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    cart = CartService.get_or_create_cart(
        user=request.user
    )

    quantity = int(
        request.POST.get(
            "quantity",
            1,
        )
    )

    CartService.update_quantity(
        cart=cart,
        product=product,
        quantity=quantity,
    )

    return redirect(
        "cart:cart_detail"
    )


@login_required
def remove_from_cart(request, product_id):
    """
    Remove a product from the user's cart.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    cart = CartService.get_or_create_cart(
        user=request.user
    )

    CartService.remove_product(
        cart=cart,
        product=product,
    )

    return redirect(
        "cart:cart_detail"
    )


@login_required
def clear_cart(request):
    """
    Remove all products from the user's cart.
    """

    cart = CartService.get_or_create_cart(
        user=request.user
    )

    CartService.clear_cart(
        cart=cart
    )

    return redirect(
        "cart:cart_detail"
    )
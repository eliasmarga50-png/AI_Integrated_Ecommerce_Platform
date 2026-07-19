


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm
from .services import OrderService


@login_required
def order_list(request):
    """
    Display all orders belonging to the logged-in user.
    """

    orders = OrderService.get_user_orders(
        user=request.user,
    )

    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders,
        },
    )


@login_required
def order_detail(request, order_number):
    """
    Display a specific order belonging to the logged-in user.
    """

    order = get_object_or_404(
        OrderService.get_order(
            order_number=order_number,
            user=request.user,
        )
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
        },
    )


@login_required
def checkout(request):
    """
    Create an Order from the user's Cart.
    """

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            cart = request.user.cart

            order = OrderService.create_order_from_cart(
                cart=cart,
                shipping_address=form.cleaned_data[
                    "shipping_address"
                ],
                shipping_city=form.cleaned_data[
                    "shipping_city"
                ],
                shipping_phone=form.cleaned_data[
                    "shipping_phone"
                ],
            )

            messages.success(
                request,
                "Your order has been placed successfully.",
            )

            return redirect(
                "orders:order_detail",
                order_number=order.order_number,
            )

    else:
        form = CheckoutForm()

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
        },
    )
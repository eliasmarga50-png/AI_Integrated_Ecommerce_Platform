


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ShopCreateForm, ShopUpdateForm
from .models import Shop
from .services import ShopService


@login_required
def shop_list(request):
    """
    Display all shops owned by the authenticated user.
    """

    shops = Shop.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "shops/shop_list.html",
        {
            "shops": shops,
        }
    )


@login_required
def shop_create(request):
    """
    Create a new shop for the authenticated user.
    """

    if request.method == "POST":
        form = ShopCreateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            ShopService.create_shop(
                owner=request.user,
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                logo=form.cleaned_data["logo"],
            )

            return redirect("shops:shop_list")

    else:
        form = ShopCreateForm()

    return render(
        request,
        "shops/shop_form.html",
        {
            "form": form,
            "page_title": "Create Shop",
        }
    )


@login_required
def shop_detail(request, slug):
    """
    Display a single shop owned by the authenticated user.
    """

    shop = get_object_or_404(
        Shop,
        slug=slug,
        owner=request.user,
    )

    return render(
        request,
        "shops/shop_detail.html",
        {
            "shop": shop,
        }
    )


@login_required
def shop_update(request, slug):
    """
    Update a shop owned by the authenticated user.
    """

    shop = get_object_or_404(
        Shop,
        slug=slug,
        owner=request.user,
    )

    if request.method == "POST":
        form = ShopUpdateForm(
            request.POST,
            request.FILES,
            instance=shop
        )

        if form.is_valid():
            ShopService.update_shop(
                shop=shop,
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                logo=form.cleaned_data["logo"],
                is_active=form.cleaned_data["is_active"],
            )

            return redirect(
                "shops:shop_detail",
                slug=shop.slug
            )

    else:
        form = ShopUpdateForm(
            instance=shop
        )

    return render(
        request,
        "shops/shop_form.html",
        {
            "form": form,
            "shop": shop,
            "page_title": "Update Shop",
        }
    )


@login_required
def shop_deactivate(request, slug):
    """
    Deactivate a shop owned by the authenticated user.
    """

    shop = get_object_or_404(
        Shop,
        slug=slug,
        owner=request.user,
    )

    if request.method == "POST":
        ShopService.deactivate_shop(
            shop=shop
        )

        return redirect(
            "shops:shop_detail",
            slug=shop.slug
        )

    return render(
        request,
        "shops/shop_confirm_deactivate.html",
        {
            "shop": shop,
        }
    )


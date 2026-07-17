

from django.contrib import messages
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
    # Optimized query by leveraging relation managers if configured,
    # or optimizing owner joins via select_related to prevent N+1 issues.
    shops = Shop.objects.filter(
    owner=request.user
    ).select_related("owner")

    return render(
        request,
        "shops/shop_list.html",
        {
            "shops": shops,
        },
    )


@login_required
def shop_create(request):
    """
    Create a new shop for the authenticated user.
    """
    if request.method == "POST":
        form = ShopCreateForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                ShopService.create_shop(
                    owner=request.user,
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    logo=form.cleaned_data["logo"],
                )
                messages.success(request, "Shop created successfully!")
                return redirect("shops:shop_list")
            except Exception as e:
                form.add_error(None, f"Could not create shop: {e}")

    else:
        form = ShopCreateForm()

    return render(
        request,
        "shops/shop_form.html",
        {
            "form": form,
            "page_title": "Create Shop",
        },
    )


@login_required
def shop_detail(request, slug):
    """
    Display a single shop owned by the authenticated user.
    """
    # Secure object lookup ensuring horizontal user authorization.
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
        },
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
        form = ShopUpdateForm(request.POST, request.FILES, instance=shop)

        if form.is_valid():
            try:
                # Service layer manages execution, updates, and handles asset cleanups safely
                updated_shop = ShopService.update_shop(
                    shop=shop,
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    logo=form.cleaned_data["logo"],
                    is_active=form.cleaned_data["is_active"],
                )
                messages.success(request, "Shop updated successfully!")
                return redirect("shops:shop_detail", slug=updated_shop.slug)
            except Exception as e:
                form.add_error(None, f"An error occurred during save: {e}")

    else:
        form = ShopUpdateForm(instance=shop)

    return render(
        request,
        "shops/shop_form.html",
        {
            "form": form,
            "shop": shop,
            "page_title": "Update Shop",
        },
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
        try:
            ShopService.deactivate_shop(shop=shop)
            messages.warning(
            request, 
            f"'{shop.name}' has been deactivated."
            )
            
            return redirect(
            "shops:shop_list"
            )
            
        except Exception as e:
            messages.error(
            request, 
            f"Could not deactivate storefront: {e}"
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
        },
    )

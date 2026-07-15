


from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm
from .models import Category, Product
from .permissions import ProductPermission
from .services import ProductService


class ProductListView(ListView):
    """
    Display all available products.
    """

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return ProductService.available_products()


class ProductDetailView(DetailView):
    """
    Display a single product.
    """

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        return ProductService.get_product(
            self.kwargs["slug"]
        )


class CategoryProductListView(ListView):
    """
    Display products belonging to one category.
    """

    model = Product
    template_name = "products/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = Category.objects.get(
            slug=self.kwargs["slug"]
        )

        return ProductService.products_by_category(
            self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = self.category

        return context


class ProductCreateView(CreateView):
    """
    Create a product.
    """

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:list")

    def dispatch(self, request, *args, **kwargs):
        ProductPermission.require(
            ProductPermission.can_create_product(
                request.user
            )
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        ProductService.create_product(form)

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    """
    Update a product.
    """

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def dispatch(self, request, *args, **kwargs):
        ProductPermission.require(
            ProductPermission.can_update_product(
                request.user
            )
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        ProductService.update_product(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "products:detail",
            kwargs={
                "slug": self.object.slug,
            },
        )


class ProductDeleteView(DeleteView):
    """
    Delete a product.
    """

    model = Product
    template_name = "products/product_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("products:list")

    def dispatch(self, request, *args, **kwargs):
        ProductPermission.require(
            ProductPermission.can_delete_product(
                request.user
            )
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        ProductService.delete_product(
            self.get_object()
        )

        return super().form_valid(form)



from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.products.views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)


class ProductURLTest(SimpleTestCase):
    """
    Tests for Products URL configuration.
    """

    def test_product_list_url(self):
        """
        '/products/' should resolve correctly.
        """
        url = reverse("products:list")

        self.assertEqual(
            url,
            "/products/",
        )

        resolver = resolve(url)

        self.assertEqual(
            resolver.func.view_class,
            ProductListView,
        )

    def test_product_detail_url(self):
        """
        Product detail URL should resolve correctly.
        """
        url = reverse(
            "products:detail",
            kwargs={
                "slug": "gaming-laptop",
            },
        )

        self.assertEqual(
            url,
            "/products/gaming-laptop/",
        )

        resolver = resolve(url)

        self.assertEqual(
            resolver.func.view_class,
            ProductDetailView,
        )

    def test_product_create_url(self):
        """
        Product create URL.
        """
        url = reverse("products:create")

        self.assertEqual(
            url,
            "/products/create/",
        )

        resolver = resolve(url)

        self.assertEqual(
            resolver.func.view_class,
            ProductCreateView,
        )

    def test_product_update_url(self):
        """
        Product update URL.
        """
        url = reverse(
            "products:update",
            kwargs={
                "slug": "gaming-laptop",
            },
        )

        self.assertEqual(
            url,
            "/products/gaming-laptop/update/",
        )

        resolver = resolve(url)

        self.assertEqual(
            resolver.func.view_class,
            ProductUpdateView,
        )

    def test_product_delete_url(self):
        """
        Product delete URL.
        """
        url = reverse(
            "products:delete",
            kwargs={
                "slug": "gaming-laptop",
            },
        )

        self.assertEqual(
            url,
            "/products/gaming-laptop/delete/",
        )

        resolver = resolve(url)

        self.assertEqual(
            resolver.func.view_class,
            ProductDeleteView,
        )
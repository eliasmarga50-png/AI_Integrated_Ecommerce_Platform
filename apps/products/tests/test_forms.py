


from decimal import Decimal

from django.test import TestCase

from apps.products.forms import CategoryForm, ProductForm
from apps.products.models import Category


class CategoryFormTest(TestCase):
    """
    Tests for CategoryForm.
    """

    def test_valid_category_form(self):
        """
        Form should accept valid data.
        """
        form = CategoryForm(
            data={
                "name": "Electronics",
            }
        )

        self.assertTrue(form.is_valid())

    def test_empty_category_name(self):
        """
        Category name is required.
        """
        form = CategoryForm(
            data={
                "name": "",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "name",
            form.errors,
        )


class ProductFormTest(TestCase):
    """
    Tests for ProductForm.
    """

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

    def get_valid_data(self):
        """
        Returns valid product data.
        """
        return {
            "category": self.category.id,
            "name": "Gaming Laptop",
            "description": (
                "A powerful gaming laptop "
                "for developers and gamers."
            ),
            "price": Decimal("1200.00"),
            "stock": 10,
            "is_available": True,
        }

    def test_valid_product_form(self):
        """
        ProductForm should accept valid data.
        """
        form = ProductForm(
            data=self.get_valid_data()
        )

        self.assertTrue(form.is_valid())

    def test_name_is_required(self):
        """
        Product name is mandatory.
        """
        data = self.get_valid_data()

        data["name"] = ""

        form = ProductForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn(
            "name",
            form.errors,
        )

    def test_price_must_be_positive(self):
        """
        Negative prices should fail.
        """
        data = self.get_valid_data()

        data["price"] = -100

        form = ProductForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn(
            "price",
            form.errors,
        )

    def test_stock_cannot_be_negative(self):
        """
        Negative stock should fail.
        """
        data = self.get_valid_data()

        data["stock"] = -5

        form = ProductForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn(
            "stock",
            form.errors,
        )

    def test_description_is_required(self):
        """
        Description is mandatory.
        """
        data = self.get_valid_data()

        data["description"] = ""

        form = ProductForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn(
            "description",
            form.errors,
        )

    def test_category_is_required(self):
        """
        Product must belong to a category.
        """
        data = self.get_valid_data()

        data["category"] = ""

        form = ProductForm(data=data)

        self.assertFalse(form.is_valid())

        self.assertIn(
            "category",
            form.errors,
        )

    def test_form_save(self):
        """
        Form should create a Product.
        """
        form = ProductForm(
            data=self.get_valid_data()
        )

        self.assertTrue(form.is_valid())

        product = form.save()

        self.assertEqual(
            product.name,
            "Gaming Laptop",
        )

        self.assertEqual(
            product.category,
            self.category,
        )

    def test_cleaned_data(self):
        """
        Cleaned data should match input.
        """
        form = ProductForm(
            data=self.get_valid_data()
        )

        self.assertTrue(form.is_valid())

        self.assertEqual(
            form.cleaned_data["name"],
            "Gaming Laptop",
        )

        self.assertEqual(
            form.cleaned_data["stock"],
            10,
        )






from django import forms

from .models import Product, ProductReview, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products.
    """

    class Meta:
        model = Product
        fields = [
            "category",
            "image",
            "name",
            "description",
            "price",
            "stock",
            "is_available",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Enter product description..."
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "min": "0",
                    "step": "0.01"
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "min": "0"
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price

    def clean_stock(self):
        stock = self.cleaned_data["stock"]

        if stock < 0:
            raise forms.ValidationError(
                "Stock cannot be negative."
            )

        return stock


class ProductReviewForm(forms.ModelForm):
    """
    Form for customer reviews.
    """

    class Meta:
        model = ProductReview
        fields = [
            "name",
            "rating",
            "comment",
        ]

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your review..."
                }
            )
        }

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

from django import forms
from .models import Category, Product, ProductReview


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "description",
        ]



from django import forms

from .models import Product, Category


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







class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "description",
        ]
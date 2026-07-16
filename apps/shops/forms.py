


from django import forms

from .models import Shop


class ShopCreateForm(forms.ModelForm):
    """
    Form used to create a new shop.
    """

    class Meta:
        model = Shop

        fields = (
            "name",
            "description",
            "logo",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your shop name",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Tell customers about your shop",
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Shop name must contain at least 3 characters."
            )

        return name


class ShopUpdateForm(forms.ModelForm):
    """
    Form used to update an existing shop.
    """

    class Meta:
        model = Shop

        fields = (
            "name",
            "description",
            "logo",
            "is_active",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Shop name must contain at least 3 characters."
            )

        return name
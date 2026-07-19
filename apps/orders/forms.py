


from django import forms


class CheckoutForm(forms.Form):
    """
    Collects shipping information during checkout.
    """

    shipping_address = forms.CharField(
        label="Shipping Address",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Enter your full shipping address",
            }
        ),
        max_length=500,
    )

    shipping_city = forms.CharField(
        label="City",
        max_length=100,
    )

    shipping_phone = forms.CharField(
        label="Phone Number",
        max_length=20,
    )

    def clean_shipping_address(self):
        """
        Validate the shipping address.
        """

        address = self.cleaned_data["shipping_address"].strip()

        if len(address) < 10:
            raise forms.ValidationError(
                "Please enter a complete shipping address."
            )

        return address

    def clean_shipping_city(self):
        """
        Validate the shipping city.
        """

        city = self.cleaned_data["shipping_city"].strip()

        if len(city) < 2:
            raise forms.ValidationError(
                "Please enter a valid city."
            )

        return city

    def clean_shipping_phone(self):
        """
        Validate the shipping phone number.
        """

        phone = self.cleaned_data["shipping_phone"].strip()

        if len(phone) < 7:
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        return phone
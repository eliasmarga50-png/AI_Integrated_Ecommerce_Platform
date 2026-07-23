


"""
Forms for the Payments application.
"""

from decimal import Decimal

from django import forms

from .models import Payment


class PaymentCreateForm(forms.ModelForm):
    """
    Form used to create a payment record.
    """

    class Meta:
        model = Payment
        fields = [
            "gateway",
        ]

    def clean_gateway(self):
        """
        Ensure a supported payment gateway is selected.
        """

        gateway = self.cleaned_data["gateway"]

        supported_gateways = {
            "chapa",
            "telebirr",
            "stripe",
            "paypal",
        }

        if gateway not in supported_gateways:
            raise forms.ValidationError(
                "Unsupported payment gateway."
            )

        return gateway


class PaymentGatewaySelectionForm(forms.Form):
    """
    Simple form for selecting
    a payment gateway.
    """

    gateway = forms.ChoiceField(
        choices=Payment.Gateway.choices,
        widget=forms.RadioSelect,
    )


class PaymentRefundForm(forms.Form):
    """
    Form used by administrators
    to request a refund.
    """

    amount = forms.DecimalField(
        min_value=Decimal("0.01"),
        decimal_places=2,
        max_digits=12,
    )

    reason = forms.CharField(
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
            }
        ),
        required=False,
    )

    def clean_reason(self):
        """
        Normalize refund reason.
        """

        reason = self.cleaned_data.get(
            "reason",
            "",
        ).strip()

        return reason



from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for creating and updating product reviews.
    """

    class Meta:
        model = Review
        fields = (
            "rating",
            "title",
            "comment",
        )
        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 5,
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "maxlength": 255,
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if not title:
            raise forms.ValidationError(
                "Title cannot be empty."
            )

        return title

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()

        if not comment:
            raise forms.ValidationError(
                "Comment cannot be empty."
            )

        return comment
        
        
        
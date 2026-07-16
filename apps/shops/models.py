


from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Shop(models.Model):
    """
    Represents a seller's shop in the AI Ecommerce platform.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shops"
    )

    name = models.CharField(
        max_length=150
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="shops/logos/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
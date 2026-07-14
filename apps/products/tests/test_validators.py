


from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.products.validators import (
    validate_description,
    validate_discount,
    validate_image_extension,
    validate_image_size,
    validate_price,
    validate_product_name,
    validate_rating,
    validate_slug,
    validate_sku,
    validate_stock,
)


class DummyImage:
    """
    Dummy image used for testing.
    """

    def __init__(self, name, size):
        self.name = name
        self.size = size


class ProductValidatorTest(SimpleTestCase):
    """
    Tests for product validators.
    """

    # -----------------------------------------
    # Product Name
    # -----------------------------------------

    def test_valid_product_name(self):
        self.assertEqual(
            validate_product_name(
                "Gaming Laptop"
            ),
            "Gaming Laptop",
        )

    def test_empty_product_name(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_product_name("")

    def test_short_product_name(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_product_name("AB")

    # -----------------------------------------
    # Price
    # -----------------------------------------

    def test_valid_price(self):
        self.assertEqual(
            validate_price(100),
            100,
        )

    def test_negative_price(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_price(-10)

    def test_zero_price(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_price(0)

    # -----------------------------------------
    # Stock
    # -----------------------------------------

    def test_valid_stock(self):
        self.assertEqual(
            validate_stock(5),
            5,
        )

    def test_negative_stock(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_stock(-1)

    # -----------------------------------------
    # Rating
    # -----------------------------------------

    def test_valid_rating(self):
        self.assertEqual(
            validate_rating(5),
            5,
        )

    def test_invalid_rating(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_rating(6)

    # -----------------------------------------
    # Discount
    # -----------------------------------------

    def test_valid_discount(self):
        self.assertEqual(
            validate_discount(25),
            25,
        )

    def test_invalid_discount(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_discount(120)

    # -----------------------------------------
    # Slug
    # -----------------------------------------

    def test_generate_slug(self):
        self.assertEqual(
            validate_slug(
                "Gaming Laptop"
            ),
            "gaming-laptop",
        )

    # -----------------------------------------
    # SKU
    # -----------------------------------------

    def test_valid_sku(self):
        self.assertEqual(
            validate_sku(
                "ELE-LAP-AB12CD"
            ),
            "ELE-LAP-AB12CD",
        )

    def test_invalid_sku(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_sku("12345")

    # -----------------------------------------
    # Image Extension
    # -----------------------------------------

    def test_valid_image_extension(self):
        image = DummyImage(
            "laptop.jpg",
            1024,
        )

        self.assertEqual(
            validate_image_extension(
                image
            ),
            image,
        )

    def test_invalid_image_extension(self):
        image = DummyImage(
            "virus.exe",
            1024,
        )

        with self.assertRaises(
            ValidationError
        ):
            validate_image_extension(
                image
            )

    # -----------------------------------------
    # Image Size
    # -----------------------------------------

    def test_valid_image_size(self):
        image = DummyImage(
            "image.jpg",
            1024,
        )

        self.assertEqual(
            validate_image_size(
                image
            ),
            image,
        )

    def test_large_image(self):
        image = DummyImage(
            "image.jpg",
            6 * 1024 * 1024,
        )

        with self.assertRaises(
            ValidationError
        ):
            validate_image_size(
                image
            )

    # -----------------------------------------
    # Description
    # -----------------------------------------

    def test_valid_description(self):
        description = (
            "This gaming laptop is "
            "perfect for developers."
        )

        self.assertEqual(
            validate_description(
                description
            ),
            description,
        )

    def test_short_description(self):
        with self.assertRaises(
            ValidationError
        ):
            validate_description(
                "Too short"
            )
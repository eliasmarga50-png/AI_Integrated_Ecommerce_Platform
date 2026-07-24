


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.forms import PaymentForm
from apps.payments.models import Payment

User = get_user_model()


class PaymentFormTests(TestCase):
    """
    Tests for the PaymentForm.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="elias",
            email="elias@example.com",
            password="password123",
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD-10001",
            total_amount=Decimal("250.00"),
            shipping_address="Addis Ababa",
            shipping_city="Addis Ababa",
            shipping_phone="0911000000",
        )

    def test_form_is_valid(self):
        """
        Form should be valid with correct data.
        """

        form = PaymentForm(
            data={
                "gateway": "chapa",
            }
        )

        self.assertTrue(form.is_valid())

    def test_gateway_is_required(self):
        """
        Gateway is a required field.
        """

        form = PaymentForm(
            data={}
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "gateway",
            form.errors,
        )

    def test_invalid_gateway_choice(self):
        """
        Invalid gateway should fail validation.
        """

        form = PaymentForm(
            data={
                "gateway": "bitcoin",
            }
        )

        self.assertFalse(form.is_valid())

    def test_gateway_choices_exist(self):
        """
        Gateway field should contain available choices.
        """

        form = PaymentForm()

        choices = [
            value
            for value, label
            in form.fields["gateway"].choices
        ]

        self.assertIn("chapa", choices)
        self.assertIn("telebirr", choices)
        self.assertIn("stripe", choices)
        self.assertIn("paypal", choices)

    def test_form_save_creates_payment(self):
        """
        Saving the form should create a Payment.
        """

        form = PaymentForm(
            data={
                "gateway": "chapa",
            }
        )

        self.assertTrue(form.is_valid())

        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway=form.cleaned_data["gateway"],
            amount=Decimal("250.00"),
            currency="ETB",
        )

        self.assertEqual(
            payment.gateway,
            "chapa",
        )

    def test_default_status_is_pending(self):
        """
        Newly created payment should be pending.
        """

        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway="stripe",
            amount=Decimal("250.00"),
            currency="ETB",
        )

        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )

    def test_transaction_reference_generated(self):
        """
        Transaction reference should be generated automatically.
        """

        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway="paypal",
            amount=Decimal("250.00"),
            currency="ETB",
        )

        self.assertTrue(
            payment.transaction_reference.startswith("PAY-")
        )

    def test_payment_belongs_to_order(self):
        """
        Payment should belong to the correct order.
        """

        payment = Payment.objects.create(
            order=self.order,
            user=self.user,
            gateway="telebirr",
            amount=Decimal("250.00"),
            currency="ETB",
        )

        self.assertEqual(
            payment.order,
            self.order,
        )




from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from .models import Stock
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class StocksTests(TransactionTestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@user.com", password="password1234")

    def test_create_new_stock(self):
        stock1 = Stock.objects.create(
            name="XYZ Amazing Company",
            short_code="XYZ",
            description="An amazing company",
            price=54.0,
        )
        self.assertEqual(stock1.name, "XYZ Amazing Company")
        self.assertEqual(stock1.short_code, "XYZ")

        with self.assertRaises(IntegrityError):
            Stock.objects.create()

        with self.assertRaises(IntegrityError):
            Stock.objects.create(name="")

        with self.assertRaises(IntegrityError):
            Stock.objects.create(name="something", short_code="")

        with self.assertRaises(IntegrityError):
            Stock.objects.create(name="something", short_code="smtn", description="")

from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from .models import Stock
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .utils import StockManager


class StocksTests(TransactionTestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@user.com", password="password1234")
        self.sm = StockManager()
        symbol = "V"
        country = "united states"
        self.stock_info = self.sm.get_stock_info(symbol, country=country)

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

    def test_stock_manager_can_create_save_to_db(self):
        # test that a new stock is created with description and up to date prices
        sm = self.sm

        stock_info = self.stock_info
        sm.save_stock(stock_info)
        stock = Stock.objects.get(name="Visa Inc Class A")
        self.assertEqual(stock.name, "Visa Inc Class A")
        self.assertEqual(stock.short_code, "V")

    def test_stock_manager_can_retrieve_dividends(self):
        # test that dividends from dividend paying stocks can be retrieved
        dividend = self.sm.get_latest_dividend(self.stock_info)
        self.assertTrue(dividend["pays_dividend"])

    def test_stock_manager_dividend_growth_rate(self):
        growth_rate = self.sm.get_dividend_growth_rate(self.stock_info)
        self.assertIsNotNone(growth_rate)

    def test_stock_manager_upcoming_events(self):
        upcoming_events = self.sm.get_stock_upcoming_events(self.stock_info)
        self.assertIsInstance(upcoming_events, list)
        self.assertIn(upcoming_events, "Event")

import investpy
import yfinance as yf
from .models import Stock

# Utils for retrieving stock information


class StockManager:
    def get_stock_info(self, symbol, country, as_json=True):

        # TODO: Use multithreading
        stock_info = investpy.get_stock_information(
            str(symbol), country, as_json=as_json
        )
        # investpy does not return stock name, use yfinance to get
        stock_ticker = yf.Ticker(symbol).info
        name = stock_ticker.get("shortName")
        stock_info["name"] = name
        stock_dividend = self.get_latest_dividend(stock_info)
        stock_info["dividend"] = stock_dividend
        return stock_info

    def get_latest_dividend(self, stock):
        stock_div = stock.get("Dividend (Yield)")
        if stock_div:
            # Dividend_amount (Yield) ==> '1.64(6.44%)'
            # search(r"(?<=\()\d+\.\d+%(?=\))", wmb_div).group()
            stock_div = stock_div.replace("%)", "").split("(")
            if "N/A" in stock_div:
                dividend = False
            else:
                dividend = True
            dividend_amount = stock_div[0]
            dividend_yield = stock_div[1]
            dividend_info = {
                "pays_dividend": dividend,
                "amount": dividend_amount,
                "yield": dividend_yield,
            }
            return dividend_info

    def get_dividend_growth_rate(self):
        pass

    def get_stock_upcoming_events(self):
        pass

    def save_stock(self, stock_obj):
        """Save a Stock to the database.

        Required stock details
        - name
        - price
        - short_code
        - description
        - dividend
        - dividend_yield
        - div_cagr
        - sector
        - next_pay_date
        - market_cap
        - payout_ratio

        """
        name = stock_obj["name"]
        price = stock_obj.get("Prev. Close")
        short_code = stock_obj.get("Stock Symbol")
        description = ""
        div_info = stock_obj.get("dividend")
        if div_info.get("pays_dividend"):
            dividend = div_info.get("amount")
            dividend_yield = div_info.get("yield")
            # dividend = stock_obj.get("Dividend (Yield)")
            # dividend_yield
            # div_cagr
            # sector
            # next_pay_date
            # market_cap
            # payout_ratio

            stk = Stock(
                name=name,
                price=price,
                short_code=short_code,
                description=description,
                dividend=dividend,
                div_yield=dividend_yield,
            )

        else:
            stk = Stock(
                name=name, price=price, short_code=short_code, description=description
            )
        stk.save()

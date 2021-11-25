import threading
from functools import partial
import concurrent.futures
import investpy
import yfinance as yf
from .models import Stock
import time

# Utils for retrieving stock information


class StockManager:
    def get_stock_name(self, symbol, country="united states"):
        """Return Stock Name."""

        stocks = investpy.get_stocks_dict(country=country)
        stock_detail = list(filter(lambda x: x["symbol"] == symbol, stocks))
        if stock_detail:
            # stock_name = stock_detail[0].get("name")
            stock_full_name = stock_detail[0].get("full_name")
            return stock_full_name

    def get_stock_info(self, symbol, country="united states", as_json=True):
        """Retrieve basic details about stock.

        This function retrieves fundamental financial information from the specified stock.

        Args:
        stock (:obj:`str`): symbol of the stock to retrieve its information from.
        country (:obj:`country`): name of the country from where the stock is from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

        Returns:
            :obj:`pandas.DataFrame` or :obj:`dict`- stock_information:
                The resulting :obj:`pandas.DataFrame` contains the information fields retrieved from Investing.com
                from the specified stock ; it can also be returned as a :obj:`dict`, if argument `as_json=True`.

                If any of the information fields could not be retrieved, that field/s will be filled with
                None values. If the retrieval process succeeded, the resulting :obj:`dict` will look like::

                    stock_information = {
                        "Stock Symbol": "AAPL",
                        "Prev. Close": 267.25,
                        "Todays Range": "263.45 - 268.25",
                        "Revenue": 260170000000.00003,
                        "Open": 267.27,
                        "52 wk Range": "142 - 268.25",
                        "EPS": 11.85,
                        "Volume": 23693550.0,
                        "Market Cap": 1173730000000.0,
                        "Dividend (Yield)": "3.08 (1.15%)",
                        "Average Vol. (3m)": 25609925.0,
                        "P/E Ratio": 22.29,
                        "Beta": 1.23,
                        "1-Year Change": "47.92%",
                        "Shares Outstanding": 4443236000.0,
                        "Next Earnings Date": "04/02/2020"
                    }

        Raises:
            ValueError: raised if any of the introduced arguments is not valid or errored.
            FileNotFoundError: raised if `stocks.csv` file was not found or errored.
            IOError: raised if `stocks.csv` file is empty or errored.
            RuntimeError: raised if scraping process failed while running.
            ConnectionError: raised if the connection to Investing.com errored (did not return HTTP 200)
        """
        start_time = time.time()

        # TODO: Use multithreading

        # with concurrent.futures.ThreadPoolExecutor() as executor:

        #     map_func = partial(
        #         investpy.get_stock_information, symbol, country, as_json=True
        #     )
        #     t1 = executor.submit(map_func)
        #     stock_info = t1.result()

        # No threading code
        stock_info = investpy.get_stock_information(
            str(symbol), country, as_json=as_json
        )

        name = self.get_stock_name(symbol, country=country)
        stock_info["name"] = name
        stock_dividend = self.get_latest_dividend(stock_info)
        stock_info["dividend"] = stock_dividend

        # Description
        result = investpy.stocks.get_stock_company_profile(symbol, country)
        company_description = result.get("desc")
        stock_info["Description"] = company_description

        # complete_time = time.time() - start_time
        # print(f"Operation took {complete_time} seconds")
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

    def get_dividend_growth_rate(self, stock_obj):
        pass

    def get_stock_upcoming_events(self, stock_obj):
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

        description = stock_obj.get("Description", "")
        div_info = stock_obj.get("dividend")
        # Check if we have this stock in the database
        try:
            stock = Stock.objects.get(short_code=short_code)
        except Stock.DoesNotExist as e:
            stock = None

        # Update or Create stock object
        if stock:
            stock.name = name
            stock.price = price
            stock.description = description
            if div_info.get("pays_dividend"):
                dividend = div_info.get("amount")
                dividend_yield = div_info.get("yield")
                stock.div_yield = dividend_yield
                stock.dividend = dividend
            stock.save()
        else:
            if div_info.get("pays_dividend"):
                dividend = div_info.get("amount")
                dividend_yield = div_info.get("yield")

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
                    name=name,
                    price=price,
                    short_code=short_code,
                    description=description,
                )
            stk.save()


def populate_db(stock):
    print(f"Processing:{stock}")
    sm2 = StockManager()
    stk_obj = sm2.get_stock_info(stock)
    sm2.save_stock(stk_obj)
    print("Saved to DB")

    # for stock in stock_list:
    #     stk_obj = sm.get_stock_info(stock)
    # print("")
    return "done"


def initialise_db(country="united states"):
    sm = StockManager()
    stock_list = investpy.stocks.get_stocks_list(country=country)
    threaded_start = time.time()
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future_to_stock = {
    #         executor.submit(populate_db, stock): stock for stock in stock_list
    #     }
    #     for future in concurrent.futures.as_completed(future_to_stock):
    #         stock = future_to_stock[future]
    #         try:
    #             data = future.result()
    #         except Exception as exc:
    #             print(f"{stock} generated an exception: {exc}")
    #         else:
    #             print(f"{data} saved")

    with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
        future_to_stock = {
            executor.submit(populate_db, stock): stock for stock in stock_list
        }
        for future in concurrent.futures.as_completed(future_to_stock):
            stock = future_to_stock[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f"{stock} generated an exception: {exc}")
            else:
                print(f"{data} saved")
    print(f"Process took {time.time() - threaded_start}s")

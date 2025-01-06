import robin_stocks
from robin_stocks import *
import robin_stocks.robinhood as r
import pyotp # type: ignore
import matplotlib.pyplot as plt # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

totp = pyotp.TOTP(os.environ["robin_mfa"]).now()

login = r.login(os.environ["robin_username"], os.environ["robin_password"], mfa_code=totp)
account_number = os.environ["tira_account_number"]

my_stocks = r.build_holdings(account_number=account_number)

print("Buying Power: " + "{:.2f}".format(float(r.profiles.load_account_profile(account_number=account_number, info='buying_power'))))

for item, data in my_stocks.items():
    current_price = float(data['price'])
    average_buy_price = float(data['average_buy_price'])
    name = item

    # Display current price with 2 decimal points
    dollar_amount = float(input(f"Enter the dollar amount you want to invest in {name} (Current Price: {current_price:.2f}): $"))
    
    order = r.order_buy_fractional_by_price(name, dollar_amount, account_number=account_number)
    
    # Display purchased quantity and price with 2 decimal points
    print("Purchased {:.2f} shares of {} at ${:.2f}".format(float(order['quantity']), name, float(order['price'])))

import robin_stocks
from robin_stocks import *
import robin_stocks.robinhood as r
import pyotp
import os
from dotenv import load_dotenv

load_dotenv()

totp = pyotp.TOTP(os.environ["robin_mfa"]).now()

login = r.login(os.environ["robin_username"], os.environ["robin_password"], mfa_code=totp)
my_stocks = r.build_holdings(account_number=os.environ["ind_account_number"])

for key, value in my_stocks.items():
    print(key, value)
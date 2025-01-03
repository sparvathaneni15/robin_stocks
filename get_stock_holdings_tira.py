import robin_stocks
from robin_stocks import *
import robin_stocks.robinhood as r
import pyotp # type: ignore
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

totp = pyotp.TOTP(os.environ["robin_mfa"]).now()

login = r.login(os.environ["robin_username"], os.environ["robin_password"], mfa_code=totp)
my_stocks = r.build_holdings(account_number=os.environ["tira_account_number"])

# Number of stocks
num_stocks = len(my_stocks)

# Create subplots (1 row for each stock)
fig, axes = plt.subplots(nrows=1, ncols=num_stocks, figsize=(8, 4))

# If there's only one stock, make axes iterable
if num_stocks == 1:
    axes = [axes]

# Loop through each stock and create a bar chart
for ax, (item, data) in zip(axes, my_stocks.items()):
    current_price = float(data['price'])
    average_buy_price = float(data['average_buy_price'])
    name = item

    # Determine bar color
    color = 'green' if current_price > average_buy_price else 'red'

    # Plot bars
    ax.bar(['Current', 'Average'], [current_price, average_buy_price], color=[color, 'blue'])
    ax.set_title(name)

# Add a single y-axis label for the entire figure
fig.text(0.04, 0.5, 'Price ($)', va='center', rotation='vertical')

# Adjust layout to avoid overlapping
plt.tight_layout(rect=[0.05, 0, 1, 1])
plt.show()
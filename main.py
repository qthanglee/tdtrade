# Import the client
import pandas as pd
from td.client import TDClient

ACCOUNT_NUMBER = "ACCOUNT_NUMBER"
CSV_FILE = "20210601.csv"
# Consumer Key
CLIENT_ID = 'CONSUMER_KEY'
# Redirect Url
REDIRECT_URL = 'REDIRECT_URL'
CRED_PATH = 'JSON_FILE_NAME'

TDSession = TDClient(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URL,
    credentials_path=CRED_PATH
)


def build_order(ticker, qty):
    data = {
        "orderType": "MARKET",
        "session": "NORMAL",
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
                    "instruction": "BUY",
                    "quantity": int(qty),
                    "instrument": {
                        "symbol": ticker,
                        "assetType": "EQUITY"
                    }
            }
        ]
    }
    return data


stocks = pd.read_csv(CSV_FILE)
df = pd.DataFrame(stocks)
orders = []
for i in range(len(df)):
    order = build_order(df.loc[i, "Ticker"], df.loc[i, "Qty"])
    orders.append(order)

TDSession.login()

for order in orders:
    order_response = TDSession.place_order(
        account=ACCOUNT_NUMBER,
        order=order
    )

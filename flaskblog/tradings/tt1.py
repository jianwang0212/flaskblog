import requests
import pandas as pd
from datetime import datetime
import ccxt
import sqlite3
import config
import settings
import os

now = datetime.utcnow()
db_path = os.path.join(os.getcwd(), 'test1.db')
print(db_path)


def get_fx(currency_f):
    fx = requests.get(
        'https://apilayer.net/api/live?access_key=a1d6d82a3df7cf7882c9dd2b35146d6e&source=USD&format=1').json()
    return fx['quotes']['USD' + currency_f.upper()]


def get_basic(time, ex, currency_f):
    now_ts = datetime.timestamp(time)
    fx_name = 'USD/' + currency_f.upper()
    fx_rate = get_fx(currency_f)
    basics = {'time': now.strftime("%y-%m-%d %H:%M:%S"),
              'utc': [now_ts],
              'exchange': [ex],
              'pair': ['ETH/' + currency_f.upper()],
              'fx': [float(fx_rate)]}
    basics = pd.DataFrame(basics)
    return basics


def get_ob(ex, pair):
    ex_instance = eval('ccxt.' + ex)()
    ob = ex_instance.fetch_order_book(pair)
    bid_px = dict(zip([str(i) + '_bid_px' for i in range(1, 6)],
                      [float(ob['bids'][i][0]) for i in range(5)]))
    ask_px = dict(zip([str(i) + '_ask_px' for i in range(1, 6)],
                      [float(ob['asks'][i][0]) for i in range(5)]))
    bid_sz = dict(zip([str(i) + '_bid_sz' for i in range(1, 6)],
                      [float(ob['bids'][i][1]) for i in range(5)]))
    ask_sz = dict(zip([str(i) + '_ask_sz' for i in range(1, 6)],
                      [float(ob['asks'][i][1]) for i in range(5)]))
    elements = {}
    elements.update(bid_px)
    elements.update(ask_px)
    elements.update(bid_sz)
    elements.update(ask_sz)
    df = pd.DataFrame({k: [v] for k, v in elements.items()})
    return df


def fetcher(exchange, now):
    ex = exchange['name']
    currency_c = 'eth'
    currency_f = exchange['currency']
    now_ts = now.timestamp()
    pair = currency_c.upper() + '/' + currency_f.upper()
    # apiInstance = settings.exchanges[ex]['init']

    basics = get_basic(now, ex, currency_f)
    ob = get_ob(ex, pair)

    df = ob
    return df


exchanges = settings.exchanges

for k, v in exchanges.items():
    exchange_name = k
    exchange = v
    df = fetcher(exchange, now)
    print(df)

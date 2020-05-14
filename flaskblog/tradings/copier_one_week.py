import requests
import pandas as pd
from datetime import datetime, timedelta
import ccxt
import sqlite3
import config
import settings
import os

now = datetime.utcnow()
db_path = os.path.join(os.getcwd(), 'test1.db')
db_path_week = os.path.join(os.getcwd(), 'main_week.db')
exchanges = settings.exchanges
def transfer_data(ex):
    conn = sqlite3.connect(db_path)
    exchange_name = ex
    
    one_week_ago = datetime.now() - timedelta(weeks = 1)
    wek_utc = one_week_ago.timestamp()*1000
    wek_utc_small = wek_utc/1000
    
    condition_open = 'utc > {}'.format(wek_utc_small)
    condition_merge = 'utc_x > {}'.format(wek_utc_small)
    condition_trades = 'utc > {}'.format(wek_utc)

    df1 = pd.read_sql_query(
        "SELECT * from {}_merge_td_bal_ods where {}".format(exchange_name, condition_merge), conn)
    df2 = pd.read_sql_query(
        "SELECT * from {}_open_order where {}".format(exchange_name, condition_open), conn)
    df3 = pd.read_sql_query(
        "SELECT * from {}_trades where {}".format(exchange_name, condition_trades), conn)
    
    
    
    conn.close()
    conn = sqlite3.connect(db_path_week)
    
    df1.to_sql('{}_merge_td_bal_ods'.format(exchange_name), conn, if_exists='replace', index=False,
                  index_label='First')
    df2.to_sql('{}_open_order'.format(exchange_name), conn, if_exists='replace', index=False,
                  index_label='First')
    df3.to_sql('{}_trades'.format(exchange_name), conn, if_exists='replace', index=False,
                  index_label='First')
    print(df1.head())
    print(df2.head())
    print(df3.head())
    conn.close()

    
for k, v in exchanges.items():
    exchange_name = k
    exchange = v
    transfer_data(exchange_name)
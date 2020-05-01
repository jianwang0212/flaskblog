import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import time
import sqlite3
import numpy as np
import math


def fig1_producer(df1, df2, df3):
  # setup
  rgba_bid = ['rgba(132, 132, 239, .9)',
              'rgba(28, 28, 221, .7)',
              'rgba(28, 28, 221, .5)',
              'rgba(28, 28, 221, .4)',
              'rgba(28, 28, 221, .2)']

  rgba_ask = ['rgba(221, 28, 86, .9)',
              'rgba(221, 28, 86, .7)',
              'rgba(221, 28, 86, .5)',
              'rgba(221, 28, 86, .4)',
              'rgba(221, 28, 86, .2)']

  rgba_bal = ['rgba(10, 10, 162, .9)',
              'rgba(10, 10, 162, .4)',
              'rgba(235, 64, 52, .9)',
              'rgba(235, 64, 52, .4)']

  # Open orders: create buy & sell column
  for side in ['buy', 'sell']:
    df2[side + '_OpenOrder_price'] = df2['OpenOrder_price']
    condition = df2['OpenOrder_side'] != side
    df2.loc[condition, side + '_OpenOrder_price'] = None

  # Trades: create buy & sell column
  for side in ['buy', 'sell']:
    df1[side + '_executed'] = df1['price']
    condition = df1['side'] != side
    df1.loc[condition, side + '_executed'] = None

  # Graph - setup traces

  # Market orderbook
  for i in [1]:
    trace_bid = go.Scatter(x=df1['time_x'],
                           y=df1[str(i) + '_bid_px'],
                           name='bid_' + str(i),
                           line={"shape": 'hv'},
                           marker_color=rgba_bid[i - 1],
                           customdata=df1[str(i) + '_bid_sz'],
                           hovertemplate="mkt_px:" + "%{y}; "
                           "sz:" + "%{customdata:.3f}<br>"
                           )
    trace_ask = go.Scatter(x=df1['time_x'],
                           y=df1[str(i) + '_ask_px'],
                           name='ask_' + str(i),
                           line={"shape": 'hv'},
                           marker_color=rgba_ask[i - 1],
                           customdata=df1[str(i) + '_ask_sz'],
                           hovertemplate="mkt_px:" + "%{y}; "
                           "sz:" + "%{customdata:.3f}<br>"
                           )

  # My open orders
  trace_open_orders_buy = go.Scatter(x=df2['time'],
                                     y=df2['buy_OpenOrder_price'],
                                     mode='markers',
                                     name='my_bid',
                                     opacity=0.8,
                                     marker=dict(color='Yellow',
                                                 size=10,
                                                 opacity=0.6,
                                                 symbol='line-ew',
                                                 line=dict(
                                                     color='LightSkyBlue',
                                                     width=4)),
                                     hovertemplate="my_bid:" + "%{y}"


                                     )
  trace_open_orders_sell = go.Scatter(x=df2['time'],
                                      y=df2['sell_OpenOrder_price'],
                                      mode='markers',
                                      name='my_ask',
                                      opacity=0.8,
                                      marker=dict(color='gold',
                                                  size=10,
                                                  opacity=0.6,
                                                  symbol='line-ew',
                                                  line=dict(
                                                      color='violet',
                                                      width=4)),
                                      hovertemplate="my_ask:" + "%{y}"


                                      )

  # My trades
  # my trades - marker setup: create a size var for marker
  sz = df1['amount'].tolist()
  sz1 = [0 if pd.isnull(x) else math.log10(float(x) + 10) * 5 for x in sz]

  trace_trades_buy = go.Scatter(x=df1['time_x'],
                                y=df1['buy_executed'],
                                name='bid_executed',
                                mode='markers',
                                marker=dict(color='LightSkyBlue',
                                            size=sz1,
                                            line=dict(
                                                color='blue',
                                                width=2)
                                            ),
                                marker_symbol='triangle-up',

                                customdata=df1['amount'],
                                hovertemplate="buy_px:" + "%{y}; "
                                "sz:" + "%{customdata}<br>"
                                )
  trace_trades_sell = go.Scatter(x=df1['time_x'],
                                 y=df1['sell_executed'],
                                 name='ask_executed',
                                 mode='markers',
                                 marker=dict(color='LightSkyBlue',
                                             size=sz1,
                                             line=dict(
                                                 color='red',
                                                 width=2)
                                             ),
                                 marker_symbol='triangle-down',

                                 customdata=df1['amount'],
                                 hovertemplate="sell_px:" + "%{y}; "
                                 "sz:" + "%{customdata}<br>"
                                 )

  # balance
  trace_bal_ff = go.Bar(x=df1['time_x'],
                        y=df1['bal_fiat_free'] / df1['1_bid_px'],
                        name='bal_fiat_free',
                        marker_color=rgba_bal[0])

  trace_bal_fu = go.Bar(x=df1['time_x'],
                        y=df1['bal_fiat_used'] / df1['1_bid_px'],
                        name='bal_fiat_used',
                        marker_color=rgba_bal[1])
  trace_bal_ef = go.Bar(x=df1['time_x'],
                        y=df1['bal_eth_free'],
                        name='bal_eth_free',
                        marker_color=rgba_bal[2])
  trace_bal_eu = go.Bar(x=df1['time_x'],
                        y=df1['bal_eth_used'],
                        name='bal_eth_used',
                        marker_color=rgba_bal[3])

  trace_bal_all = go.Scatter(x=df1['time_x'],
                             y=(df1['bal_eth_total'] * df1['1_bid_px'] +
                                df1['bal_fiat_total']) / df1['fx_x'],
                             name='bal_all($)')

  # Group traces to fig
  fig1_sub1_traces = [trace_bid, trace_ask, trace_open_orders_buy, trace_open_orders_sell,
                      trace_trades_buy, trace_trades_sell]
  fig1_sub2_traces = [trace_bal_ff, trace_bal_fu,
                      trace_bal_ef, trace_bal_eu]

  fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                       specs=[[{"secondary_y": True}],
                              [{"secondary_y": True}]],
                       subplot_titles=("Market orderbook & my orders/trades (Local currency)", "My holding position (left-ETH) & total balance(right-USD)"))

  for i in range(len(fig1_sub1_traces)):
    fig1.add_trace(fig1_sub1_traces[i],
                   row=1, col=1)

  for i in range(len(fig1_sub2_traces)):
    fig1.add_trace(fig1_sub2_traces[i],
                   row=2, col=1)

  fig1.add_trace(trace_bal_all,
                 row=2, col=1, secondary_y=True)
  fig1.update_layout(barmode='stack')
  fig1.update_layout(title='Historical time series')
  return fig1


def fig2_producer(df1, df2, df3):
  # Fig 2 Current dash board
  # Bal pie chart
  pie_labels = ['fiat_free', 'fiat_used', 'eth_free', 'eth_used']
  pie_values = [df1['bal_fiat_free'].iloc[-1] / df1['1_bid_px'].iloc[-1], df1['bal_fiat_used'].iloc[-1] / df1['1_bid_px'].iloc[-1],
                df1['bal_eth_free'].iloc[-1], df1['bal_eth_used'].iloc[-1]]

  trace_pie_bal = go.Pie(
      labels=pie_labels, values=pie_values, title='Balance in ETH', hole=0.4,
      textinfo='label+percent')

  # order book info

  boop = df2['buy_OpenOrder_price']
  c_boop = boop.loc[~boop.isnull()].iloc[-1]
  soop = df2['sell_OpenOrder_price']
  c_soop = soop.loc[~soop.isnull()].iloc[-1]

  ob_y_bid = [df1['1_bid_px'].iloc[-1], df1['2_bid_px'].iloc[-1],
              df1['3_bid_px'].iloc[-1], df1['4_bid_px'].iloc[-1], df1['5_bid_px'].iloc[-1]]
  ob_y_ask = [df1['1_ask_px'].iloc[-1], df1['2_ask_px'].iloc[-1],
              df1['3_ask_px'].iloc[-1], df1['4_ask_px'].iloc[-1], df1['5_ask_px'].iloc[-1]]

  trace_c_ords_bid = go.Scatter(
      x=[1] * len(ob_y_bid), y=ob_y_bid, mode="markers", marker_symbol='line-ew',
      marker_line_color="midnightblue", marker_color="lightskyblue",
      marker_line_width=3, marker_size=150, name='mkt_bid')
  trace_c_ords_ask = go.Scatter(
      x=[1] * len(ob_y_ask), y=ob_y_ask, mode="markers", marker_symbol='line-ew',
      marker_line_color="red", marker_color="red",
      marker_line_width=3, marker_size=150, name='mkt_ask')

  trace_c_ords_my_bid = go.Scatter(
      x=[1], y=[c_boop], mode="markers", marker_symbol='diamond-wide',
      marker_line_color="gold", marker_color="blue",
      marker_line_width=2, marker_size=15, name='my_bid')
  trace_c_ords_my_ask = go.Scatter(
      x=[1], y=[c_soop], mode="markers", marker_symbol='diamond-wide',
      marker_line_color="gold", marker_color="red",
      marker_line_width=2, marker_size=15, name='my_ask')

  fig2 = make_subplots(rows=1, cols=2,
                       specs=[[{"type": "domain"}, {"type": "xy"}]],
                       subplot_titles=("Holdings", "Order book position"))
  fig2.add_trace(trace_pie_bal, row=1, col=1)
  fig2.add_trace(trace_c_ords_bid, row=1, col=2)
  fig2.add_trace(trace_c_ords_ask, row=1, col=2)
  fig2.add_trace(trace_c_ords_my_bid, row=1, col=2)
  fig2.add_trace(trace_c_ords_my_ask, row=1, col=2)

  fig2.update_layout(title='Current orders and positions')
  return fig2


# to calculate the total bal container
def nearest(items, pivot):
  return min(items, key=lambda x: abs(x - pivot))


def cal_bal_usd(x):
  return (x['bal_fiat_total'] + x['bal_eth_total'] * x['1_bid_px']) / x['fx_x']


def pnl_to_string(amt, pct, mkt_pct, rlt_pct):
  amt = '$' + amt.round().to_string().split()[1] + '/'
  pct = (100 * pct).round(2).to_string().split()[1] + '%/'
  mkt_pct = (100 * mkt_pct).round(2).to_string().split()[1] + '%/'
  rlt_pct = (100 * rlt_pct).round(2).to_string().split()[1] + '%'
  s = amt + pct + mkt_pct + rlt_pct
  return s


def pnl(df, time):

  now = df['time_x'].iloc[-1]
  previous = now - dt.timedelta(hours=time)
  index = nearest(df['time_x'], previous)
  condition = df['time_x'] == index
  x_data = df[condition]  # previous time data
  y_data = df.iloc[-1]  # current time data
  x_bal = cal_bal_usd(x_data)
  y_bal = cal_bal_usd(y_data)
  amt = y_bal - x_bal
  pct = amt / x_bal
  mkt_amt = (y_data['1_bid_px'] - x_data['1_bid_px'])
  mkt_pct = mkt_amt / (x_data['1_bid_px'])  # market price change in percent
  rlt_amt = amt - mkt_amt * 0.5
  rlt_pct = pct - mkt_pct * 0.5
  s = pnl_to_string(amt, pct, mkt_pct, rlt_pct)
  return s


def register_callbacks(dashapp):

  @dashapp.callback(
      [Output('table_openorders', 'data'),
       Output('table_trades', 'data'),
       Output('table_openorders', 'columns'),
       Output('table_trades', 'columns'),
       Output('g1', 'figure'),
       Output('g2', 'figure'),
       Output("live_clock", "children"),
       Output("5h_pnl", "children"),
       Output("1d_pnl", "children"),
       Output("1w_pnl", "children")],
      [Input('interval-component', 'n_intervals'),
       Input('exchange_options', 'value')])
  def update_tables_graphs(_, value):
    print('Receive new data and updating')

    db_path = os.path.join(os.getcwd(), 'flaskblog/tradings/test1.db')
    exchange_name = value
    conn = sqlite3.connect(
        db_path, check_same_thread=False)
    df1 = pd.read_sql_query(
        "SELECT * from {}_merge_td_bal_ods".format(exchange_name), conn)
    df2 = pd.read_sql_query(
        "SELECT * from {}_open_order".format(exchange_name), conn)
    df3 = pd.read_sql_query(
        "SELECT * from {}_trades".format(exchange_name), conn)
    conn.close()

    df1['time_x'] = df1['time_x'].apply(
        lambda x: dt.datetime.strptime(x, "%y-%m-%d %H:%M:%S"))
    # tables
    ## tables - data
    tbl_my_trades = df3[['time', 'type', 'takerOrMaker', 'side', 'amount', 'price',
                         'fee_fiat', 'fee_pct']]
    tbl_my_orders = df2[['time', 'OpenOrder_side', 'OpenOrder_price',
                         'OpenOrder_amount', 'OpenOrder_filled', 'OpenOrder_remaining',
                         'OpenOrder_fee']]
    tbl_my_trades = tbl_my_trades.tail().iloc[::-1]
    tbl_my_orders = tbl_my_orders.tail().iloc[::-1]

    # tables - column
    columns_trades = [{"name": i, "id": i} for i in tbl_my_trades.columns]
    columns_orders = [{"name": i, "id": i} for i in tbl_my_orders.columns]

    # graphs

    fig1 = fig1_producer(df1, df2, df3)
    fig2 = fig2_producer(df1, df2, df3)

    # update live clock
    new_time = dt.datetime.now().strftime("%H:%M:%S")

    # update the profit container
    # v1 = pnl(df1, 5)
    v_5h_pnl = pnl(df1, 5)
    v_1d_pnl = pnl(df1, 24)
    v_1w_pnl = pnl(df1, 24 * 7)

    return tbl_my_orders.to_dict('records'), tbl_my_trades.to_dict('records'), columns_orders, columns_trades, fig1, fig2, new_time, v_5h_pnl, v_1d_pnl, v_1w_pnl

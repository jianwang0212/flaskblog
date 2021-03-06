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

exchanges = ['indodax',
             'bitbay']
# Layout (static theme)
layout = html.Div(
    className="row",
    children=[
        # Left Panel Div
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.Img(
                            className="logo",
                            src='/tradings/assets/logo_dashboard.jpg'
                        ),
                        html.H6(className="title-header",
                                children="CRYPTO MONITOR"),
                        html.P([
                            """
                            This app continually queries/update market orderbook (5 level bids/ask) every minute,
                            my balance and my current open order every minute, my historical trades every 30
                            minutes in different exchanges. """, html.Br(), html.Br(),
                            """

                            The first panel shows the comparison between the historical market orderbookv (red/blue
                            thin line) and my orders (blur dash) and my executed trades (triangles). """, html.Br(), html.Br(),
                            """

                            The second panel shows my current position in ETH and Fiat for a specific exchange (left pie fig),
                            and my latest open orders compare to the current 5 level market orderbook (right fig). """, html.Br(), html.Br(),
                            """

                            The third panel shows my latest 5 trades and latest 5 open orders in a specific exchange.  """, html.Br(), html.Br(),
                            """

                            P.s: You can use the top-right tools in each interactive graph to zoom in/out, change hovers, and pan.  """

                        ]
                        ),
                    ],
                ),
                # Ask Bid Currency Div
                html.Div(
                    className="div-currency-toggles",
                    children=[
                        html.P(className="three-col", children="Last update"),
                        html.P(
                            id="live_clock",
                            className="three-col",
                            children=dt.datetime.now().strftime("%H:%M:%S"),
                        ),
                    ],
                ),
            ],
        ),
        # Right Panel Div
        html.Div(
            className="nine columns div-right-panel",
            children=[
                html.Div(
                    className="row",
                    children=[dcc.Dropdown(
                        id='exchange_options',
                        options=[{'label': i, 'value': i} for i in exchanges],
                        value='bitbay'),
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="5h_pnl"),
                                     html.P("5h pnl(amt/pct/mkt_pct/rlt_pct)")],
                                    id="5hpnl",
                                    className="mini_container",
                                ),
                                # html.Div(
                                #     [html.H6(id="10h_pnl"),
                                #      html.P("10h pnl(amt/pct/mkt_pct/rlt_pct)")],
                                #     id="10hpnl",
                                #     className="mini_container",
                                # ),
                                html.Div(
                                    [html.H6(id="1d_pnl"),
                                     html.P("1d pnl(amt/pct/mkt_pct/rlt_pct)")],
                                    id="1dpnl",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="1w_pnl"),
                                     html.P("1w pnl(amt/pct/mkt_pct/rlt_pct)")],
                                    id="1wpnl",
                                    className="mini_container",
                                ),
                                # html.Div(
                                #     [html.H6(id="1m_pnl"),
                                #      html.P("1m pnl(amt/pct/mkt_pct/rlt_pct)")],
                                #     id="1mpnl",
                                #     className="mini_container",
                                # ),
                                # html.Div(
                                #     [html.H6(id="YTD_pnl"),
                                #      html.P("YTD pnl(amt/pct/mkt_pct/rlt_pct)")],
                                #     id="YTDpnl",
                                #     className="mini_container",
                                # ),

                            ],
                            className="row container-display",
                    ),
                        dcc.Graph(id='g1'),
                        dcc.Graph(id='g2')],
                ),

            ],
        ),
        html.H2('My latest open orders'),
        dash_table.DataTable(id='table_openorders',
                             style_as_list_view=True,
                             style_cell={'padding': '5px'},
                             style_header={
                                 'backgroundColor': 'white',
                                 'fontWeight': 'bold'
                             }),
        html.H2('My latest trades'),
        dash_table.DataTable(id='table_trades',
                             style_as_list_view=True,
                             style_cell={'padding': '5px'},
                             style_header={
                                 'backgroundColor': 'white',
                                 'fontWeight': 'bold'
                             }),

        dcc.Interval(id='interval-component',
                     interval=500 * 1000, n_intervals=0),


    ]
)

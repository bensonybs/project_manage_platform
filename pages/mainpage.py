from dash import Dash, html, dcc, dash_table, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import modules.database as database  # modules/database.py

dash.register_page(__name__, path='/', name='首頁')

page_header = dbc.Row(dbc.Col(dcc.Markdown(children='# 首頁')))
page_content = dbc.Row([
    dbc.Col(dcc.Markdown(children='main page with information of the website'),
            width=6),
    dbc.Col(dcc.Markdown(children='content2'), width=12),
    dbc.Col(dcc.Markdown(children='content3'), width=12)
])
layout = dbc.Container([page_header, page_content], fluid=True)
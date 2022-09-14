from dash import Dash, html, dcc, dash_table, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import modules.database as database  # modules/database.py


dash.register_page(__name__, name='統計圖表')
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='# 儀表板')))
page_content = dbc.Row(dbc.Col(dcc.Markdown(children='dashboard of projects')))
layout = dbc.Container([page_header, page_content], fluid=True)
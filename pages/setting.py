import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash import dash_table
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
import modules.database as database  # modules/database.py


dash.register_page(__name__, name='設定')

page_header = dbc.Row(dbc.Col(dcc.Markdown(children='# 設定')))
page_content = dbc.Row(dbc.Col(dcc.Markdown(children='user setting')))
layout = dbc.Container([page_header, page_content], fluid=True)
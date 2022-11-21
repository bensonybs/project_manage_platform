import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
from modules.database import mongoDatabase, projects, project_details, production_emission  # modules/database.py


dash.register_page(__name__, name='統計圖表')
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='### 儀表板')))
page_content = dbc.Row(dbc.Col(dcc.Markdown(children='dashboard of projects')))
layout = dbc.Container([page_header, page_content], fluid=True)
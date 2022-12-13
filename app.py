import dash
from dotenv import load_dotenv
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output
from dash import dash_table
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
load_dotenv('./.env')
app = Dash(__name__,
           use_pages=True,
           external_stylesheets=[dbc.themes.FLATLY],
           title='碳排減量')


# Style
global_style = {'font-family': 'cursive'}


# Dash components
navbar = dbc.NavbarSimple(
    children=[
        # Disable link of setting
        dbc.NavItem(dbc.NavLink(page['name'], href=page["relative_path"]))
        for page in dash.page_registry.values()
    ],
    brand="南亞塑膠碳排減量專案管理平台",
    brand_style={
        'font-size': '40px'
    },
    brand_href="/",
    color="primary",
    dark=True,
    sticky='top',
    fluid=True
)
footer = dbc.Row(dbc.Col(html.Footer(children='資訊應用組')))


# Layout
app.layout = dbc.Container([navbar, dash.page_container, footer], fluid=True, style=global_style)

if __name__ == '__main__':
    app.run_server(debug=True)

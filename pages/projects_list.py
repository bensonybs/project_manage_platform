from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import modules.database as database  # modules/database.py

app = Dash(name=__name__, external_stylesheets=[dbc.themes.FLATLY])

# Table data source
df = database.projects

# Style
global_style = {}
table_header_style = {'font-family': 'cursive'}
table_data_style = {
    'whiteSpace': 'normal',
    'height': 'auto',
    'font-family': 'cursive'
}

# Dash components
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='# 碳排減量案件彙總')))
control_panel = dbc.Row([
    dbc.Col(dbc.Button('開啟', color='secondary'), width=2),
    dbc.Col(dbc.Button(children='Save', color='danger'), width=3)
])
table = dbc.Row(
    dbc.Col(
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{
                "name": i + 'test',
                "id": i,
                "deletable": True,
                "selectable": True,
                "hideable": True
            } if i == "iso_alpha3" or i == "year" or i == "id" else {
                "name": i,
                "id": i,
                "deletable": True,
                "selectable": True,
                "hideable": True
            } for i in df.columns],
            editable=True,
            row_deletable=True,
            filter_action=
            "native",  # allow filtering of data by user ('native') or not ('none')
            sort_action=
            "native",  # enables data to be sorted per-column by user or not ('none')
            sort_mode="single",  # sort across 'multi' or 'single' columns
            column_selectable=
            "multi",  # allow users to select 'multi' or 'single' columns
            row_selectable=
            "multi",  # allow users to select 'multi' or 'single' rows
            selected_columns=[],  # ids of columns that user selects
            selected_rows=[],  # indices of rows that user selects
            page_action=
            "native",  # all data is passed to the table up-front or not ('none')
            page_current=0,  # page number that user is on
            page_size=20,  # number of rows visible per page
            style_data=
            table_data_style,  # overflow cells' content into multiple lines
            style_header=table_header_style)))

# Dash layout
app.layout = dbc.Container([page_header, control_panel, table], fluid=False)

# Run
if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
from modules.database import mongoDatabase, excelDataSource # modules/database.py
# Data source
projects = excelDataSource.getDataFrameFromSheet('projects')
project_details = excelDataSource.getDataFrameFromSheet('project_details')
production_emission = excelDataSource.getDataFrameFromSheet('production_emission')
df = production_emission
df['年份'] = df['年份'].astype(str)

dash.register_page(__name__, name='統計圖表')
# Components
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='### 儀表板')))
page_content = dbc.Row(dbc.Col(dcc.Markdown(children='dashboard of projects')))
# Bar chart (x: 各廠(2020, 2021); y:排放量, 產量)
dropdown_filters = dbc.Col(dcc.Dropdown(
    options=[division for division in df['事業部'].unique()],
    id='dropdown_filter',
    placeholder='事業部'),
                           class_name='col-1')
division = '纖維部'
condition = df['事業部'] == division
df = df[condition] 
fig = px.histogram(df, x="年份", y="碳排放量",
             color='年份', barmode='group', facet_col='廠處')
barChart = dcc.Graph(figure=fig, id='')
# Callback
# @callback(Output('data-table', 'data'), Input('dropdown_filter', 'value'))
# def filterTable(division):
#     # Filter data table via division selected by user.
#     if division:
#         filterCondition = df['事業部'] == division
#         dff = df[filterCondition].to_dict('records')
#         return dff
#     return df.to_dict('records')  # Return full dataframe back

# Layout
layout = dbc.Container([page_header, dropdown_filters, barChart, page_content], fluid=True)
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
from modules.database import mongoDatabase, excelDataSource  # modules/database.py
# Data source
projects = excelDataSource.getDataFrameFromSheet('projects')
project_details = excelDataSource.getDataFrameFromSheet('project_details')
production_emission = excelDataSource.getDataFrameFromSheet(
    'production_emission')
df = production_emission
df['年份'] = df['年份'].astype(str)

dash.register_page(__name__, name='統計圖表')
"""
Components
1. 事業部下拉選單
2. 各廠碳排兩年度比較圖
3. 各廠產量兩年度比較圖
4. 各廠產量影響碳排及實際碳排比較表
"""
page_header = dcc.Markdown(children='### 儀表板')

# 1. 事業部下拉選單
division_filter = dcc.Dropdown(
    options=[division for division in df['事業部'].unique()],
    id='division_filter',
    placeholder='事業部')
department_filter = dcc.Dropdown(
    options=[division for division in df['廠處'].unique()],
    id='department_filter',
    placeholder='廠處',
     multi=True,)

# 2. 各廠碳排兩年度比較圖
header2 = dcc.Markdown('#### 碳排放量')
emission_per_department = dcc.Graph(figure={}, id='emission_per_department')
# 3. 各廠產量兩年度比較圖
header3 = dcc.Markdown('#### 產量')
production_per_department = dcc.Graph(figure={},
                                      id='production_per_department')
# 4. 各廠產量影響碳排及實際碳排比較表
header4 = dcc.Markdown('#### 產量影響及實際減排')
adjust_emission_per_department = dcc.Graph(figure={},
                                           id='adjust_emission_per_department')

# Bar chart (x: 各廠(2020, 2021); y:排放量, 產量)

# Callback
@callback([Output('department_filter', 'options'), Output('department_filter', 'value')], Input('division_filter', 'value'))
def filterDepartment(division):
    if not division:
        division = '塑膠一部' # 預設先顯示塑一部資料
    condition1 = df['事業部'] == division
    dff = df[condition1]
    options = dff['廠處'].unique()
    values = options
    return options, values

@callback([Output('emission_per_department', 'figure'), Output('production_per_department', 'figure')], [Input('division_filter', 'value'), Input('department_filter', 'options')])
def showChart(division, department):
    # 根據下拉選單選擇的事業部篩選資料(產量、碳排放)並呈現
    if not division:
        division = '塑膠一部' # 預設先顯示塑一部資料
    print(department)
    condition = (df['事業部'] == division) and (df['廠處'].isin(department))
    dff = df[condition].to_dict('records')

    # 2. 各廠碳排兩年度比較圖
    emission_per_department_fig = px.histogram(dff,
                   x="年份",
                   y="碳排放量",
                   color='年份',
                   barmode='group',
                   facet_col='廠處')
    # 3. 各廠產量兩年度比較圖
    production_per_department_fig = px.histogram(dff,
                   x="年份",
                   y="產量",
                   color='年份',
                   barmode='group',
                   facet_col='廠處')
    return emission_per_department_fig, production_per_department_fig

# Layout
layout = dbc.Container(
    [dbc.Row(dbc.Col(page_header)),
    dbc.Row([dbc.Col(division_filter, class_name='col-2 m-1'), dbc.Col(department_filter, class_name='col-2 m-1')]),
    dbc.Row(dbc.Col(header2)),
    dbc.Row(dbc.Col(emission_per_department)),
    dbc.Row(dbc.Col(header3)),
    dbc.Row(dbc.Col(production_per_department)),
    dbc.Row(dbc.Col(header4)),
    dbc.Row(dbc.Col(adjust_emission_per_department))], fluid=True)

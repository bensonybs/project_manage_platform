import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash import dash_table
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
df['單位碳排'] = df['碳排放量'] / df['產量']
df = df.round({'產量': 0, '單位碳排': 2})
# Constants
DEFAULT_DIVISION = '塑膠一部'
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
    multi=True,
)

# 2. 各廠碳排兩年度比較圖
header2 = dcc.Markdown('#### 碳排放量')
emission_per_department = dcc.Graph(figure={}, id='emission_per_department')
# 3. 各廠產量兩年度比較圖
header3 = dcc.Markdown('#### 產量')
production_per_department = dcc.Graph(figure={},
                                      id='production_per_department')
# 4. 各廠產量影響碳排及實際碳排比較表
header4 = dcc.Markdown('#### 產量影響及實際減排')
adjust_emission_per_department = html.Div(children={},
                                         id='adjust_emission_per_department')

# Bar chart (x: 各廠(2020, 2021); y:排放量, 產量)


# Callback
@callback([
    Output('department_filter', 'options'),
    Output('department_filter', 'value')
], Input('division_filter', 'value'))
def filterDepartment(division):
    if not division:
        division = DEFAULT_DIVISION  # 預設先顯示塑一部資料
    condition1 = df['事業部'] == division
    dff = df[condition1]
    options = dff['廠處'].unique()
    values = options
    return options, values


@callback([
    Output('emission_per_department', 'figure'),
    Output('production_per_department', 'figure'),
    Output('adjust_emission_per_department', 'children')
], [Input('division_filter', 'value'),
    Input('department_filter', 'value')])
def showChart(division, department):
    # 根據下拉選單選擇的事業部篩選資料(產量、碳排放)並呈現
    if not division:
        division = DEFAULT_DIVISION  # 預設先顯示塑一部資料
    dff = df.query('事業部 == @division & 廠處.isin(@department)')
    dff_records = dff.to_dict('records')
    # 2. 各廠碳排兩年度比較圖
    emission_per_department_fig = px.histogram(dff_records,
                                               x="年份",
                                               y="碳排放量",
                                               color='年份',
                                               barmode='group',
                                               facet_col='廠處')
    # 3. 各廠產量兩年度比較圖
    production_per_department_fig = px.histogram(dff_records,
                                                 x="年份",
                                                 y="產量",
                                                 color='年份',
                                                 barmode='group',
                                                 facet_col='廠處')
    # 4. 產量影響及實際碳排比較表
    dff1 = dff[dff['年份'] == '2020'].loc[:, ['廠處代號', '年份', '產量', '碳排放量', '單位碳排']]
    dff2 = dff[dff['年份'] == '2021']
    
    global_style = {'font-family': 'cursive'}
    dff_merged = dff2.merge(dff1, on='廠處代號', suffixes=('(2021)', '(2020)'))
    del dff_merged['年份(2021)']
    del dff_merged['年份(2020)']
    dff_merged['差異'] = dff_merged['碳排放量(2021)'] - dff_merged['碳排放量(2020)']
    dff_merged['產量影響'] = (dff_merged['產量(2021)'] *
                         dff_merged['單位碳排(2020)']) - dff_merged['碳排放量(2020)']
    dff_merged['實際增減排'] = dff_merged['差異'] - dff_merged['產量影響']
    dff_merged = dff_merged.round({'產量影響': 0, '實際增減排': 0})
    dff_merged = dff_merged.loc[:, ['廠處', '產量(2020)', '碳排放量(2020)', '單位碳排(2020)', '產量(2021)', '碳排放量(2021)', '單位碳排(2021)', '差異', '產量影響', '實際增減排', '備註']]
    table_columns = [{
        "name": column,
        "id": column,
        "deletable": False,
        "selectable": False,
        "hideable": False,
        "type": 'numeric',
        "editable": False,
        "format": Format().group(True),
    } if column in ['產量(2020)', '碳排放量(2020)', '單位碳排(2020)', '產量(2021)', '碳排放量(2021)', '單位碳排(2021)', '差異', '產量影響', '實際增減排'] else {
        "name": column,
        "id": column,
        "deletable": False,
        "selectable": False,
        "hideable": False,
    } for column in dff_merged.columns]
    table = dash_table.DataTable(
        id='data-table',
        data=dff_merged.to_dict('records'),
        columns=table_columns,
        editable=True,
        filter_action=
        "native",  # allow filtering of data by user ('native') or not ('none')
        sort_action=
        "native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="multi",  # sort across 'multi' or 'single' columns
        hidden_columns=['id'],
        column_selectable=
        False,  # allow users to select 'multi' or 'single' columns
        row_selectable=False,  # allow users to select 'multi' or 'single' rows
        cell_selectable=False,
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action=
        "native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=50,  # number of rows visible per page
        style_data=global_style,  # overflow cells' content into multiple lines
        style_header=global_style,
        style_data_conditional=[{
            'if': {
                'filter_query': '{單位碳排(2021)} > {單位碳排(2020)}',
                'column_id': '單位碳排(2021)'
            },
            'backgroundColor': 'yellow',
            'color': 'black'
        }],
        tooltip_header={
            '差異': '與前一年相比，大於零為增排，反之則為減排，為[產量影響]及[實際增減排]兩者相加',
            '產量影響': '受產量變化影響而產生的碳排放',
            '實際增減排': '因單位碳排降低而獲得的減排效益'
        }
    )

    return emission_per_department_fig, production_per_department_fig, table


# Layout
layout = dbc.Container([
    dbc.Row(dbc.Col(page_header)),
    dbc.Row([
        dbc.Col(division_filter, class_name='col-2 m-1'),
        dbc.Col(department_filter, class_name='col-2 m-1')
    ]),
    dbc.Row(dbc.Col(header4)),
    dbc.Row(dbc.Col(adjust_emission_per_department, width=8), justify='center'),
    dbc.Row(dbc.Col(header2)),
    dbc.Row(dbc.Col(emission_per_department)),
    dbc.Row(dbc.Col(header3)),
    dbc.Row(dbc.Col(production_per_department)),
],
                       fluid=True)

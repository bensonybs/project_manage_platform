import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash import dash_table
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
import modules.database as database  # modules/database.py

dash.register_page(__name__, name='減量案件明細表')
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
# Functions
def createInputForm():
    for column in df.columns:
        print(column) 
    form = html.Div(
        [dbc.Label(children=column, html_for=column),
        dbc.Input(type='text', id=column, placeholder="預設字元")]
        for column in df.columns
    ) 
    return form
# Dash components
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='# 碳排減量案件彙總')),
                      style={'potision': 'sticky'})


control_panel = dbc.Row([
    dbc.Col(dbc.Button(children='新增案件', color='secondary', id='create-button'),
            width='auto'),
    dbc.Col(dbc.Button(children='篩選', color='info', id='collapse-button'),
            width='auto'),
    dbc.Col(dbc.DropdownMenu(label="顯示案件筆數",
                                      children=[
                                          dbc.DropdownMenuItem(number)
                                          for number in [10, 50, 100, 500, 1000, 2000]
                                      ],
                                      color='warning'), width='auto'),
    # dbc.Col(dbc.Button(children='匯出Excel(開發中)',
    #                    color='danger',
    #                    id='export-button',
    #                    class_name='disabled'),
    #         width='auto'),
    dbc.Col(dbc.Button(
        children='表格使用說明', color='primary', id='description-button'),
            width='auto')
],
                        class_name='mb-2')
# Modal
# description_modal = dbc.Modal([
#     dbc.ModalHeader(dbc.ModalTitle('說明')),
#     dbc.ModalBody([createInputForm()])
# ],
#                               id='description-modal',
#                               is_open=False,
#                               backdrop='static',
#                               size='lg')
project_detail_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('案件明細')),
    dbc.ModalBody([dcc.Markdown('''
    1. 點擊篩選按鈕開啟篩選欄位
    2. 可直接在表格中修改資料，修改完畢後請點擊 **儲存**，若直接離開此頁則資料不會儲存
    3. 雙擊該列即可開啟案件減碳量明細
    ''')])
],
                              id='description-modal',
                              is_open=True)
# Collapse dorpdown filters
dropdown_filters = dbc.Row(
    dbc.Col(
        dbc.Collapse(dbc.DropdownMenu(label="事業部",
                                      children=[
                                          dbc.DropdownMenuItem(division)
                                          for division in df['事業部'].unique()
                                      ],
                                      color='secondary'),
                     is_open=True)))

# Data table
table_columns = [{
    "name": column,
    "id": column,
    "deletable": False,
    "selectable": False,
    "hideable": False,
    "type": 'numeric',
    "format": Format().group(True)
} if column == '投資費用(千元)' else {
    "name": column,
    "id": column,
    "deletable": False,
    "selectable": False,
    "hideable": False,
} for column in df.columns]
table_columns[0]['hideable'] = True # Set column 'id' hideable
table = dbc.Row(
    dbc.Col(
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=table_columns,
            editable=False,
            filter_action=
            "native",  # allow filtering of data by user ('native') or not ('none')
            sort_action=
            "native",  # enables data to be sorted per-column by user or not ('none')
            sort_mode="multi",  # sort across 'multi' or 'single' columns
            column_selectable=
            "multi",  # allow users to select 'multi' or 'single' columns
            hidden_columns=['id'],
            row_selectable=
            False,  # allow users to select 'multi' or 'single' rows
            selected_columns=[],  # ids of columns that user selects
            selected_rows=[],  # indices of rows that user selects
            page_action=
            "native",  # all data is passed to the table up-front or not ('none')
            page_current=0,  # page number that user is on
            page_size=50,  # number of rows visible per page
            style_data=
            table_data_style,  # overflow cells' content into multiple lines
            style_header=table_header_style,
        )))
# Callback

# Dash layout
layout = dbc.Container([page_header, control_panel, dropdown_filters, project_detail_modal, table],
                       fluid=True)

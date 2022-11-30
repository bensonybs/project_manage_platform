import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash import dash_table
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
import data.seeds.projectSeeder as seedData
from modules.database import mongoDatabase, excelDataSource # modules/database.py
dash.register_page(__name__, name='減量案件明細')
# Table data source
projects = excelDataSource.getDataFrameFromSheet('projects')
project_details = excelDataSource.getDataFrameFromSheet('project_details')
production_emission = excelDataSource.getDataFrameFromSheet('production_emission')
df = projects

# Style
global_style = {}
table_header_style = {'font-family': 'cursive'}
table_data_style = {
    'whiteSpace': 'normal',
    'height': 'auto',
    'font-family': 'cursive'
}


class Utility:
    """Utility Functions"""
    def createForm(self, columns, values):
        """create form"""
        formChildren = []
        for column in columns:
            title = dbc.Col(dbc.Label(children=column, html_for=column),
                            width='2')
            input = dbc.Col(dbc.Textarea(id=column, value=values[column]),
                            width='6')
            formChildren.append(dbc.Row([title, input], class_name='mb-1'))
        form = dbc.Form(children=formChildren, id='project-form')
        return form

    def createDictWithoutValue(self, keys):
        return {key: None for key in keys}


utility = Utility()
# Dash components
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='### 碳排減量案件彙總')),
                      style={'potision': 'sticky'})
# Control Panel
page_size_dropdown = dbc.Col(dcc.Dropdown(
    placeholder="顯示案件筆數",
    options=[number for number in [10, 50, 100, 500, 1000, 2000]],
    id='page_size_dropdown'),
                             class_name='col-2')
dropdown_filters = dbc.Col(dcc.Dropdown(
    options=[division for division in df['事業部'].unique()],
    id='dropdown_filter',
    placeholder='事業部篩選'),
                           class_name='col-2')
control_panel = html.Div([
    dbc.Row([
        dbc.Col(dbc.Button(
            children='新增案件', color='success', id='create-button'),
                width='auto'),
        dbc.Col(dbc.Button(
            children='表格使用說明', color='info', id='description-button', n_clicks=0),
                width='auto')
    ],
            class_name='mb-2'),
    dbc.Row([page_size_dropdown, dropdown_filters])
])
# Modal
project_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('案件內容')),
    dbc.ModalBody(children=[], id='project-modal-body'),
    dbc.ModalFooter(children=[dbc.Button('儲存', id='save')])
],
                          is_open=False,
                          size='lg',
                          id='project-modal')
description_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('使用說明')),
    dbc.ModalBody([
        dcc.Markdown('''
    1. 點擊[事業部篩選]按鈕篩選事業部
    2. 點擊[顯示案件筆數]調整表格每頁顯示案件筆數，預設為50筆
    2. 可直接在表格中修改資料，修改完畢後請點擊 **儲存**，若直接離開此頁則資料不會儲存
    ''')
    ])
],
                              id='description-modal',
                              is_open=False)
modal_pannel = html.Div([project_modal, description_modal])
# Data table
table_columns = [{
    "name": column,
    "id": column,
    "deletable": False,
    "selectable": False,
    "hideable": False,
    "type": 'numeric',
    "editable": False,
    "format": Format().group(True),
} if column == '投資費用(千元)' else {
    "name": column,
    "id": column,
    "deletable": False,
    "selectable": False,
    "hideable": False,
} for column in df.columns]
table_columns[0]['hideable'] = True  # Set column 'id' hideable
table = dbc.Row(
    dbc.Col(
        dash_table.DataTable(
            id='data-table',
            data=df.to_dict('records'),
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
            row_selectable=
            False,  # allow users to select 'multi' or 'single' rows
            cell_selectable=False,
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
@callback([
    Output('project-modal-body', 'children'),
    Output('project-modal', 'is_open'),
    Output('create-button', 'n_clicks')
], [Input('create-button', 'n_clicks'),
    Input('data-table', 'is_focused')],
          [State('data-table', 'active_cell'),
           State("data-table", "data")],
          prevent_initial_call=True)
def createOrUpdateData(n_clicks, is_focused, active_cell, table_data):
    columns = df.columns
    if n_clicks:
        rowData = utility.createDictWithoutValue(columns)
    elif is_focused:
        rowData = table_data[active_cell['row']]
    else:
        raise dash.exceptions.PreventUpdate
    print(rowData)
    inputForm = utility.createForm(columns, rowData)
    modalOpen = True
    n_clicks = None
    return inputForm, modalOpen, n_clicks

@callback([Output('description-modal', 'is_open'), Output('description-button', 'n_clicks')], Input('description-button', 'n_clicks'), prevent_initial_call=True)
def showDescriptionModal(n_clicks):
    if n_clicks > 0:
        return True, n_clicks

@callback(Output('data-table', 'data'), Input('dropdown_filter', 'value'))
def filterTable(division):
    # Filter data table via division selected by user.
    if division:
        filterCondition = df['事業部'] == division
        dff = df[filterCondition].to_dict('records')
        return dff
    return df.to_dict('records')  # Return full dataframe back


@callback(Output('data-table', 'page_size'),
          Input('page_size_dropdown', 'value'),
          prevent_initial_call=True,
          suppress_callback_exceptions=True)
def changeTablePageSize(size):
    if size:
        return size
    return 50  # Default page size is 50


# Dash layout
layout = dbc.Container(
    [page_header, control_panel, modal_pannel, table],
    fluid=True)

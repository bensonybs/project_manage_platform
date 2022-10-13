from datetime import datetime
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
# Component
show_announcement_button = dbc.Button('顯示公告', n_clicks=0, id='show_announcement_button')
create_announcement_button = dbc.Button(children='新增公告',
                                       color='secondary',
                                       class_name='me-1',
                                       n_clicks=0,
                                       id='create_announcement_button')
create_announcement_modal = dbc.Modal(dbc.Form([
    dbc.ModalHeader(dbc.ModalTitle('新增首頁公告')),
    dbc.ModalBody(children=[
            dbc.Label('標題'),
            dbc.Input(placeholder='請輸入公告標題', id='announcement_title', required=True, value=''),
            dbc.Label('內容'),
            dbc.Textarea(placeholder='請輸入內容', id='announcement_content', required=True, value='')
    ]),
    dbc.ModalFooter(children=[
        dbc.Button('儲存公告', n_clicks=0, id='save_announcement_button', type='submit')
    ])
]),
                                     is_open=False,
                                     id='announcement_modal')
create_success_modal = dbc.Modal(children='儲存成功',
                                 is_open=False,
                                 id='save_success')
announcement_panel = dbc.Row([
    dbc.Col(show_announcement_button),
    dbc.Col(create_announcement_button),
    dbc.Col(create_announcement_modal),
    dbc.Col(create_success_modal)
])
page_header = dbc.Row(dbc.Col(dcc.Markdown(children='### 設定')))

page_content = dbc.Row(dbc.Col(dcc.Markdown(children='')))


# Callback
@callback([
    Output('create_announcement_button', 'n_clicks'),
    Output('save_announcement_button', 'n_clicks'),
    Output('announcement_modal', 'is_open'),
    Output('announcement_title', 'value'),
    Output('announcement_content', 'value')
], [
    Input('create_announcement_button', 'n_clicks'),
    Input('save_announcement_button', 'n_clicks')
], [State('announcement_title', 'value'), State('announcement_content', 'value'), State('announcement_modal', 'is_open')], prevent_initial_call=True)
def createNewAnnouncement(create_n_clicks, save_n_clicks, title, content, is_open):
    resetClicks = 0
    resetValue = ''
    if create_n_clicks: # Open input modal
        is_open = not is_open
    if save_n_clicks: # Save announcement to mongodb
        if title == '' or content == '':
          # Do nothing
          pass
        else:
          announcement = [{
            'title': title,
            'content': content,
            'date': datetime.now()
          }]
          collection_name = 'announcements'
          database.insertDocuments(announcement, collection_name)
          print(f'Save announcement: {announcement}')
          title = resetValue
          content = resetValue
          is_open = not is_open
    return resetClicks, resetClicks, is_open, title, content


#Layout
layout = dbc.Container([page_header, announcement_panel, page_content],
                       fluid=True)

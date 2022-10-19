from ast import Div
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State
from dash import dash_table
from dash.dash_table.Format import Format, Group
import plotly.express as px
import pandas as pd
import modules.database as database  # modules/database.py

dash.register_page(__name__, path='/', name='公告')


# Callback
# @callback([
#     Output(announcemnets_panel, 'children'),
#     Output(updateButton, 'n_clicks')
# ], Input(updateButton, 'n_clicks'))
# def updateAnnouncement(n_clicks):
#     resetClicks = 0
#     announcement_cards = []
#     if n_clicks > 0:
#         announcements = database.getDocuments('announcements', sorting={'date': 'desc'})
#         announcement_cards = [
#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader(
#                         [
#                             html.Div(annoucement['title']),
#                             html.Div(annoucement['date'].strftime('%Y/%m/%d'))
#                         ],
#                         class_name='d-flex justify-content-between'),
#                     dbc.CardBody(annoucement['content'])
#                 ], class_name='h-100')) for annoucement in announcements
#         ]
#     return announcement_cards, resetClicks
def showLayout():
    """一般layout變數可以直接設定為components，但此處為了可以在每次重新整理時至資料庫抓取最新資料。因此將layout指定為函式showLayout"""
    # Components
    # User announcement
    announcements = database.getDocuments('announcements',
                                          sorting={'date': 'desc'})
    announcement_cards = [
        dbc.Col(
            dbc.Card([
                dbc.CardHeader([
                    html.Div(annoucement['title']),
                    html.Div(annoucement['date'].strftime('%Y/%m/%d'))
                ],
                               class_name='d-flex justify-content-between'),
                dbc.CardBody(annoucement['content'])
            ],
                     class_name='h-100')) for annoucement in announcements
    ]
    announcemnets_panel = dbc.Row(children=announcement_cards,
                                  id='announcements_panel',
                                  class_name='row-cols-3 g-2')
    page_header = dbc.Row(dbc.Col(dcc.Markdown(children='### 首頁')))

    return dbc.Container([page_header, announcemnets_panel], fluid=True)
layout = showLayout

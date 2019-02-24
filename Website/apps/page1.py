#dash imports 
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np

from app import app
import os
from apps.Components import header

from apps.Components import colorscale

#read data here

#do data processing (consider using seperate python file if needed)

#layout
#use flex display, do not set margins in pixels if avoidable
page1Layout = html.Div(
    style={
        'display':'flex-inline',
        'flex-direction':'column',
        'justify-content':'space-between',
    },
    children=[
        #start row 1
        html.Div(
            style={
                'background-color':colorscale.bg,
                'display':'flex',
                'flex-direction':'row',
                'margin-bottom':'2%',
            },
            children=[
                #start sample graph 1
                html.Div(
                    style={
                        'flex':'1',
                        'height':'600px',
                        'background-color':colorscale.divBG,
                        'margin-left':'2%',
                        'margin-right':'1%',
                    },
                    children=[
                        dcc.Graph(
                            id='example-graph-1',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {
                                    'title': 'Dash Data Visualization'
                                }
                            }
                        )
                    ]
                ),
                #end sample graph 1
                #start sample graph 2
                html.Div(
                    style={
                        'flex':'1',
                        'height':'600px',
                        'background-color':colorscale.divBG,
                        'margin-left':'1%',
                        'margin-right':'2%'
                    },
                    children=[
                        dcc.Graph(
                            id='example-graph-2',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {
                                    'title': 'Dash Data Visualization'
                                }
                            }
                        )
                    ]
                )
                #end sample graph 2
            ]
        ),
        #end row 1
        #start row 2
        html.Div(
            style={
                'background-color':colorscale.bg,
                'display':'flex',
                'flex-direction':'row',
                'margin-bottom':'2%',
            },
            children=[
                #start sample graph 1
                html.Div(
                    style={
                        'flex':'1',
                        'height':'600px',
                        'background-color':colorscale.divBG,
                        'margin-left':'2%',
                        'margin-right':'1%',
                    },
                    children=[
                        dcc.Graph(
                            id='example-graph-1',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {
                                    'title': 'Dash Data Visualization'
                                }
                            }
                        )
                    ]
                ),
                #end sample graph 1
                #start sample graph 2
                html.Div(
                    style={
                        'flex':'1',
                        'height':'600px',
                        'background-color':colorscale.divBG,
                        'margin-left':'1%',
                        'margin-right':'2%'
                    },
                    children=[
                        dcc.Graph(
                            id='example-graph-2',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {
                                    'title': 'Dash Data Visualization'
                                }
                            }
                        )
                    ]
                )
                #end sample graph 2
            ]
        )
        #end row 2
    ]

)
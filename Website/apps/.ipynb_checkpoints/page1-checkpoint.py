#dash imports 
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import pybedtools

from pybedtools.contrib import plotting


import pandas as pd
import numpy as np

from app import app
import os
import io
import base64
from apps.Components import header

from apps.Components import colorscale




import plotly.graph_objs as go

#do data processing (consider using seperate python file if needed)
def processData(list_of_BEDs, minimum_overlap_amount, chromosome):
    overlap_only = list_of_BEDs[0].window(list_of_BEDs[1:], w=minimum_overlap_amount).overlap(cols=[2, 3, 8, 9])
    overlap_df = pd.read_table(overlap_only.fn, names=['chrom', 'start', 'end', 'name', 'score', 'strand', 'thickStart', 'thickEnd', 'detail_2', 'blockCount', 'blockSizes', 'blockStarts'])
    overlap_df.columns = ['start', 'end', 'details_1', 'score', 'strand', 'thickStart', 'thickEnd', 'detail_2', 'blockCount', 'blockSizes', 'blockStarts', 'score_2']
    overlap_df['chrom'] = overlap_df.index
    overlap_df.index = list(range(0,overlap_df.shape[0]))
    overlap_df = overlap_df.drop(['score', 'strand', 'thickStart', 'thickEnd', "blockCount", "blockSizes", "blockStarts", "score_2"], axis = 1)
    bed_raw = []
    for BED in list_of_BEDs:
        bed_raw.append(BED.fn)
    result_temp = pybedtools.BedTool()
    result = result_temp.multi_intersect(i=bed_raw)
    result_df = result.to_dataframe()
    result_df = result_df[result_df['start'].isin(overlap_df['start'])]
    result_df['score_split'] = result_df['score'].str.split(",")
    result_df['score_split_length'] = [len(x) for x in result_df['score_split']]
    result_df = result_df.drop(['score_split'], axis = 1)
    #df = df[df['score_split_length'] >= 2]
    result_df['width_region'] = result_df['end'] - result_df['start']
    result_df['height'] = 3
    result_df[result_df['chrom'] == chromosome]
    print(result_df)
    colorbar_ticks = np.linspace(min(result_df["score_split_length"]),max(result_df["score_split_length"]),max(result_df["score_split_length"]))
    return overlap_df, result_df, colorbar_ticks

#read data here
BedTools_OBJS = []
BEDs = os.listdir('Data')
for file in BEDs:
    BedTools_OBJS.append(pybedtools.BedTool("Data/{}".format(file)))

chromosome = 'chr1'
minOverlap = 100
overlap, result, ticks_colorbar = processData(BedTools_OBJS, minOverlap, chromosome)


#layout
#use flex display, do not set margins in pixels if avoidable
page1Layout = html.Div(
    style={
        'display':'flex-inline',
        'flex-direction':'column',
        'justify-content':'space-between',
    },
    children=[
        html.Div(
            style={
                'display':'flex',
                'margin-bottom':'20px',
                'flex-direction':'column',
            },
            children=[
                html.Div(
                    style={
                        'flex':'3',
                        'margin-right':'10px',
                        'order':2,
                    },
                    children=[
                        #start graph
                        dcc.Graph(
                            id = 'chromosome-visualization',
                            figure=go.Figure(
                                 data = [
                                     go.Bar(
                                         x = result['start'],
                                         y = result['height'],
                                         text = result['score_split_length'],
                                         hoverinfo = 'text',
                                         width = result['end'] - result['start'],
                                         marker = dict(
                                             color = result['score_split_length'],
                                             colorbar=dict(
                                                     title='Number of Overlaps',
                                                     tickvals=ticks_colorbar
                                              )
                                         )
                                     ),
                                 ],
                                 layout = go.Layout(
                                     title = "Chromosome : Cross-BED Overlap",
                                     xaxis=dict(
                                         autorange=True,
                                         showgrid=False,
                                         zeroline=False,
                                         showline=True,
                                         showticklabels=True
                                     ),
                                     yaxis=dict(
                                         autorange=True,
                                         showgrid=False,
                                         zeroline=False,
                                         showline=False,
                                         ticks='',
                                         showticklabels=False
                                     )
                                     )
                                     ),
                        ),
                        #end graph
                    ]
                ),
                html.Div(
                    style={
                        'flex':'2',
                        'margin-left':'10px',
                        'flex-order':1,
                    },
                    children=[
                        html.Div(
                            style={
                                'flex-direction':'column',
                                'display':'flex-inline',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'flex':'1',
                                        'margin-top':'10px',
                                    },
                                    children=[
                                        #data upload position
                                        dcc.Upload(
                                            multiple=True,
                                            id = 'upload-data',
                                            children = html.Div(
                                                [
                                                    'Upload your input data here'
                                                ]
                                            ),
                                            style={
                                                'height': '60px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin': '10px'
                                            },
                                        )
                                        #end data upload position 
                                    ]
                                ),
                                html.Div(
                                    style={
                                        'flex':'1',
                                        'margin-bottom':'10px',
                                    },
                                    children=[
                                        #checklist
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id = 'chormosome-dropdown',
                                                    options=[
                                                        {'label': 'Chromosome 1', 'value': 'chr1'},
                                                        {'label': 'Chromosome 2', 'value': 'chr2'},
                                                        {'label': 'Chromosome 3', 'value': 'chr3'},
                                                        {'label': 'Chromosome 4', 'value': 'chr4'},
                                                        {'label': 'Chromosome 5', 'value': 'chr5'},
                                                        {'label': 'Chromosome 6', 'value': 'chr6'},
                                                        {'label': 'Chromosome 7', 'value': 'chr7'},
                                                        {'label': 'Chromosome 8', 'value': 'chr8'},
                                                        {'label': 'Chromosome 9', 'value': 'chr9'},
                                                        {'label': 'Chromosome 10', 'value': 'chr10'},
                                                        {'label': 'Chromosome 11', 'value': 'chr11'},
                                                        {'label': 'Chromosome 12', 'value': 'chr12'},
                                                        {'label': 'Chromosome 13', 'value': 'chr13'},
                                                        {'label': 'Chromosome 14', 'value': 'chr14'},
                                                        {'label': 'Chromosome 15', 'value': 'chr15'},
                                                        {'label': 'Chromosome 16', 'value': 'chr16'},
                                                        {'label': 'Chromosome 17', 'value': 'chr17'},
                                                        {'label': 'Chromosome 18', 'value': 'chr18'},
                                                        {'label': 'Chromosome 19', 'value': 'chr19'},
                                                        {'label': 'Chromosome 20', 'value': 'chr20'},
                                                        {'label': 'Chromosome 21', 'value': 'chr21'},
                                                        {'label': 'Chromosome 22', 'value': 'chr22'},
                                                        {'label': 'Chromosome X', 'value': 'chrX'},
                                                        {'label': 'Chromosome Y', 'value': 'chrY'},
                                                        {'label': 'Chromosome M', 'value': 'chrM'}
                                                    ],
                                                    multi = False, 
                                                    value = 'chr1',
                                                ),
                                                
                                            ]
                                        )
                                        #end checklist
                                    ]
                                ),
                                html.Div(
                                    style={
                                        'flex':1,
                                        'margin-left':'20px',
                                        'margin-bottom':'10px',
                                        'margin-top':'10px',
                                    },
                                    children=[
                                        html.Div(
                                            style={
                                                'flex-direction':'column',
                                            },
                                            className='row',
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.H6('Enter minimum intersection of base pairs:'),
                                                        dcc.Input(
                                                            id = 'pair-limit',
                                                            type = 'int',
                                                            value = '1',
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.H6('Enter minimum number of trial intersections:'),
                                                        dcc.Input(
                                                            id='bed-files',
                                                            type = 'int',
                                                            value = '2',
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                        ),

                    ]
                )
            ]
        ),
        html.Div(id='output-data-upload'),
        html.Div(
            children=[
                html.H2(
                    'Background Information:',
                    style={
                        'font-size':'35px',
                        'margin-left':'2%',
                        'font-weight':'bold',
                    }
                ),
                html.Ul(
                    children=[
                        html.Li('Huntington\'s Disease is caused by a mutation in the HD gene, located on chromosome 4. The HD gene is a sequence of a nucleotide triplet repeat of the base sequence CAG. In a person without a mutation in their HD gene, this CAG sequence repeats 10 to 35 times. This sequence codes for a protein called the huntingtin protein. This protein is needed for the function of neurons in the brain. If this sequence repeats more than 40 times, the huntingtin protein is longer and leads to the disruption and death of certain areas in the brain.  ', className='analysis-findings list-group-item'),
                        html.Li('Other areas of the genome can affect how much of the HD gene is activated and transposed into proteins. When experiments are run to see which areas of the genome interact with the area of chromosome 4 that codes for the HD gene, the results are slightly different every time due to the numerous factors that affect the protocol of collecting data. These factors are nearly impossible to control for and therefor will have an effect on the results of which base pairs interact with the HD gene. These factors include differences in the cells (for example, different stages in the cell cycle) and imperfections in the process of handling DNA.  ', className='analysis-findings list-group-item'),
                        html.Li('This visualizer helps show the overlap between different experimental trials. Each trial is its own BED file. The more overlap, the more confident that researchers can be that a portion of the genome have an interaction with the HD gene. In our visualization, we started with the three BED files given to us. In this program, you can upload additional BED files of genomic data.  ', className='analysis-findings list-group-item'),
                    ],
                )                                    
            ]
        )
    ],
)

@app.callback(
    Output(component_id='chromosome-visualization', component_property='figure'),
    [Input(component_id='chormosome-dropdown', component_property='value'),
     Input(component_id = 'pair-limit', component_property = 'value')]
)
def update_graph(value1, value2):
    chromosome = value1
    minOverlap = value2
    print('value1: ' + value1)
    print('value2: ' + value2)
    overlap, result, ticks_colorbar = processData(BedTools_OBJS, int(minOverlap), chromosome)
    figure=go.Figure(
            data = [
                go.Bar(
                    x = result['start'],
                    y = result['height'],
                    text = result['score_split_length'],
                    hoverinfo = 'text',
                    width = result['end'] - result['start'],
                    marker = dict(
                        color = result['score_split_length'],
                        colorbar=dict(
                                title='Number of Overlaps',
                                tickvals=ticks_colorbar
                        )
                    )
                ),
            ],
            layout = go.Layout(
                title = "Chromosome : Cross-BED Overlap".format(),
                xaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    showticklabels=True
                ),
                yaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    ticks='',
                    showticklabels=False
                )
                )
                ),
        #end graph
    return figure

# def parse_contents(contents, filenames):
#     print(len(contents))
#     data=[]
#     for x in range (0, len(contents)):
#         content_string = contents[x]
#         try:
#             data.append(pybedtools.BedTool(
#                 io.StringIO(content_string)
#             ))
#             #read in data
#             pass
#         except Exception as e:
#             print(e)
#             return html.Div([
#                 'There was an error processing this file'
#             ])
#     print('success: ' + len(data))
#     return
#     #edit layout bois

 
# @app.callback(Output('output-data-upload', 'children'),
#               [Input('upload-data', 'contents')],
#               [State('upload-data', 'filename'),
#               State('upload-data', 'last_modified')])

# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(list_of_contents, list_of_names)
#         ]
#         return children
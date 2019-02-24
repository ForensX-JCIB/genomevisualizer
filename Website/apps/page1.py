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
def processData(list_of_BEDs, minimum_overlap_amount, chromosome, minBEDCount):
    overlap_only = list_of_BEDs[0].window(list_of_BEDs[1:], w=minimum_overlap_amount).overlap(cols=[2, 3, 8, 9])
    overlap_df = pd.read_table(overlap_only.fn,header=None)
    overlap_df['chrom'] = overlap_df.index
    overlap_df.index = list(range(0,overlap_df.shape[0]))
    overlap_df=overlap_df.iloc[:,0:2]
    overlap_df.columns = ["chrom","start"] 
    overlap_df.head()
    bed_raw = []
    for BED in list_of_BEDs:
        bed_raw.append(BED.fn)
    result_temp = pybedtools.BedTool()
    result = result_temp.multi_intersect(i=bed_raw)
    result_df = result.to_dataframe(header=None)
    result_df = result_df.iloc[:,0:5]
    print(result_df.head())
    result_df.columns = ['chrom', 'start', 'end', 'strand', 'score']
    print(result_df.head())
    result_df = result_df[result_df['start'].isin(overlap_df['start'])]
    result_df['score_split'] = result_df['score'].str.split(",")
    result_df['score_split_length'] = [len(x) for x in result_df['score_split']]
    result_df = result_df.drop(['score_split'], axis = 1)
    result_df['width_region'] = result_df['end'] - result_df['start']
    result_df['height'] = 3
    result_df = result_df[result_df['chrom'] == chromosome]
    result_df = result_df[result_df['score_split_length'] >= minBEDCount]
    ticks_colorbar = [x for x in range(min(result_df["score_split_length"]),max(result_df["score_split_length"])+1)]
    result_df = result_df[result_df['score_split_length'] >= int(minBEDCount)]
    result_df.to_csv('exportedData//export_BED.bed', header=False, index=False)
    result_df = result_df[result_df['chrom'] == chromosome]
    result_df.to_csv('exportedData//export_BED_{}_overlapbp{}_minBEDcount{}.bed'.format(chromosome, minimum_overlap_amount, minBEDCount), header=False, index=False)
    return overlap_df, result_df, ticks_colorbar



#read data here
BedTools_OBJS = []
BEDs = os.listdir('Data')
for file in BEDs:
    BedTools_OBJS.append(pybedtools.BedTool("Data/{}".format(file)))

# chromosome = 'chr1'
# minOverlap = 100
# overlap, result, ticks_colorbar = processData(BedTools_OBJS, minOverlap, chromosome, 2)


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
                    id='chromosome-visualization',
                    style={
                        'flex':'3',
                        'margin-right':'10px',
                        'order':2,
                    },
                    children=[ 
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
                                'display':'flex',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'flex':'1',
                                        'margin-bottom':'10px',
                                    },
                                    children=[
                                        html.Div(
                                            style={
                                                'width':'30%',
                                                'border-bottom':'3px solid black',
                                                'margin-bottom':'10px',
                                            },
                                            children=[
                                                html.H6('Any .bed files in the Data folder will be used in the visualizations.'),
                                                html.H6('Processed data from the .bed files can be found in the exportedData folder.')
                                            ],
                                        ),
                                        #checklist
                                        html.Div(
                                            style={
                                                'width':'30%'
                                            },
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
                                                    style={
                                                        'width':'30%'
                                                    },
                                                    children=[
                                                        html.H6('Enter minimum overlap of base pairs:'),
                                                        dcc.Input(
                                                            id = 'pair-limit',
                                                            type = 'int',
                                                            value = '1',
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    style={
                                                        'width':'30%'
                                                    },
                                                    children=[
                                                        html.H6('Enter minimum number of trial intersections across all BED files:'),
                                                        html.Div(
                                                            style={
                                                                'width':'90%',
                                                            },
                                                            children=[
                                                                dcc.Slider(
                                                                id='intersect-slider',
                                                                min = 2,
                                                                max = len(BEDs),
                                                                step = 1,
                                                                marks = {
                                                                i: str(i) for i in range(len(BEDs)+1)
                                                                },
                                                                value = 2,
                                                            ),
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            html.Div([
                                                html.A('Download BED file for intersections', id =  'my-link')
                                            ], style = {
                                                'margin-top': 50
                                            })
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
    ],
)

@app.callback(
    Output(component_id='chromosome-visualization', component_property='children'),
    [Input(component_id='chormosome-dropdown', component_property='value'),
     Input(component_id = 'pair-limit', component_property = 'value'),
     Input(component_id = 'intersect-slider', component_property = 'value')]
)


def update_graph(chromosomeInput, overlapInput, bedInput):
    print("IN CALLBACK")
    chromosome = chromosomeInput
    minOverlap = int(overlapInput)
    BED_count = int(bedInput)
    print('Chromosome: ' + chromosome)
    print('Overlap: ' + str(minOverlap))
    overlap1, result1, ticks_colorbar1 = processData(BedTools_OBJS, minOverlap, chromosome, BED_count)
    text_matrix = ["Start: {}bp, End: {}bp <br>Number of Intersections: {}, Percent of Files: {:.2f}%</br>".format(result1['start'][index], result1['end'][index], result1['score_split_length'][index], result1['score_split_length'][index]*100/len(BEDs)) for index, row in result1.iterrows()]
    # Start, End\nNumber of Intersections
    return dcc.Graph(
        figure=go.Figure(
            data = [
            go.Bar(
                x = result1['start'],
                y = result1['height'],
                text=text_matrix,
                hoverinfo = 'text',
                width = result1['end'] - result1['start'],
                marker = dict(
                    color = result1['score_split_length'],
                    colorbar=dict(
                            title='Number of Overlaps',
                            tickvals=ticks_colorbar1
                    )
                )
            ),
        ],
        layout = go.Layout(
            height=600,
            title = "Chromosome {}: Cross-BED Overlap. Minimum Overlap: {}bp, Intersection Minimum: {}".format(chromosome[3], minOverlap, BED_count),
            xaxis=dict(
                title =  "Basepair (bp)",
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
    )


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
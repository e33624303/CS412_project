import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import plotly.express as px
import plotly as py
import plotly.graph_objs as go 
import pandas as pd
import numpy as np
import random
from data import data_init

colors = {
    'background': '#222222',
    'text': '#FF4500'
}

df = data_init()
columns = {
    'Country': 0,
    'Coutry Code': 1,
    'Region': 2,
    'Sub-Region': 3,
    'Population': 4, #int
    'Density': 5, #int
    'Land Area': 5, #int
    'Fert Rate': 6,  #percentage
    'Urban Pop': 7, #percentage
    'Years': 8, #category
    'Deaths': 9, #int
    'Household Pollution': 10,  #float
    'Ambient Matter Pollution': 11, #float
    'Ambient Ozone Pollution': 12, #float
    'Air Pollution': 13, #float
    'Outdoor Air Pollution': 14 #float
}

order = []
for i in range(-9, 9):
    for j in range(-5, 5):
        order.append([i*i+j*j, i, j])
order.sort()

def generate_graph(yaxis_value):
    if not(yaxis_value in columns):
        yaxis_value = 'Population'
    #print(yaxis_value)
    fig = px.bar(df, x="Country", y=yaxis_value, color="Years", barmode="group")
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor='#191970',
        font_color=colors['text']
    )
    #print("update barchart")
    return fig

def generate_scatter(scatterx, scattery):
    if not(scatterx in columns):
        scatterx = 'Population'
    if not(scattery in columns):
        scattery = 'Air Pollution'
    scatterPlot = px.scatter(data_frame=df, x=scatterx, y=scattery, color='Years', hover_name='Country')
    scatterPlot.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    scatterPlot.update_xaxes(title=scatterx)
    scatterPlot.update_yaxes(title=scattery)
    return scatterPlot

def generate_wordcloud(column):
    if not(column in columns):
        column = 'Population'
    df_ = df.groupby(['Country']).mean()
    max_val = np.max([d for d in df_[column]])
    min_val = np.min([d for d in df_[column]])
    normalized_val = [(int)((d-min_val)/(max_val-min_val)*25)+15 for d in df_[column]]
    avg = [{'Country':'', 'average': d} for d in df_[column]]
    id = 0
    for country in df_.index:
        avg[id]['Country'] = country
        id += 1
    normalized_val.sort(reverse=True)
    sorted_val = sorted(avg, key = lambda i: i['average'], reverse=True)
    fcolor = [py.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(len(normalized_val))]
    wordcloud_d = go.Scatter(
                       #x=list(range(len(normalized_val))),
                       #y=random.choices(range(len(normalized_val)), k=len(normalized_val)),
                       x=[order[i][1] for i in range(len(avg))],
                       y=[order[i][2] for i in range(len(avg))],
                       mode='text',
                       text= [sorted_val[i]['Country'] for i in range(len(avg))],
                       #text = [d for d in df_.index],
                       marker={'opacity': 0.3},
                       #textfont = {'size': [random.randint(15, 35) for i in range(len(rating_avg))]})
                       textfont={'size': normalized_val, 'color': fcolor})
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    wordcloud = go.Figure(data=[wordcloud_d], layout=layout)
    wordcloud.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    return wordcloud

def generate_worldmap(column):
    if not(column in columns):
        column = 'Population'
    fig = px.scatter_geo(df, locations='Coutry Code',size=column)
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor='#191970',font_color=colors['text'])
    return fig

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(
        children='CS412 Group 5 - Applying Data Mining into the Field of Global Air Pollution Data',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(children='Ching-Hsi Chen(chchen8), Ping-Hung Lai(phlai2)',
        style={
            'textAlign': 'center',
        }
    ), 
    html.H2(children='Bar Chart:', style={
        'textAlign': 'left',
    }),
    html.Div([
        html.H3(children='Y-axis:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='yaxis_value',
            options=[{'label': i, 'value': i} for i in ['Population','Density','Land Area','Fert Rate','Urban Pop','Deaths','Household Pollution','Ambient Matter Pollution','Ambient Ozone Pollution','Air Pollution','Outdoor Air Pollution']],
            value='Population',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    dcc.Graph(
        id='bar-chart',
        figure=generate_graph('Population')
    ),
    html.H2(children='Scatter Plot:'),
    html.Div([
        html.H3(children='X-axis:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='scatterx',
            options=[{'label': i, 'value': i} for i in ['Population','Density','Land Area','Fert Rate','Urban Pop','Deaths','Household Pollution','Ambient Matter Pollution','Ambient Ozone Pollution','Air Pollution','Outdoor Air Pollution']],
            value='Population',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Div([
        html.H3(children='Y-axis', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='scattery',
            options=[{'label': i, 'value': i} for i in ['Population','Density','Land Area','Fert Rate','Urban Pop','Deaths','Household Pollution','Ambient Matter Pollution','Ambient Ozone Pollution','Air Pollution','Outdoor Air Pollution']],
            value='Air Pollution',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'left': '65%', 'position': 'absolute'}),
    dcc.Graph(
        id='scatter-plot',
        figure=generate_scatter('Population', 'Air Pollution'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
    html.H2(children='Word Cloud:', style={
        'textAlign': 'left',
    }),
    html.Div([
        html.H3(children='Value:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='Val',
            options=[{'label': i, 'value': i} for i in ['Population','Density','Land Area','Fert Rate','Urban Pop','Deaths','Household Pollution','Ambient Matter Pollution','Ambient Ozone Pollution','Air Pollution','Outdoor Air Pollution']],
            value='Population',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    dcc.Graph(
        id='word-cloud',
        figure=generate_wordcloud('Population'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
    html.H2(children='World Map Scatter Plot:', style={
        'textAlign': 'left',
    }),
    html.Div([
        html.H3(children='Value:', style={
            'textAlign': 'left',
        }),
        dcc.Dropdown(
            id='Val1',
            options=[{'label': i, 'value': i} for i in ['Population','Density','Land Area','Fert Rate','Urban Pop','Deaths','Household Pollution','Ambient Matter Pollution','Ambient Ozone Pollution','Air Pollution','Outdoor Air Pollution']],
            value='Population',
            style={ 'color': '#000000','background-color': '#A0A0A0'} 
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),
    dcc.Graph(
        id='worldmap',
        figure=generate_worldmap('Population'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
], style={'background-color': '#191970', 'color': '#FF4500', 'font-family': '"Trebuchet MS", sans-serif'})

@app.callback(
    Output('bar-chart', 'figure'),
    Input('yaxis_value', 'value'))
def update_graph(yaxis_value):
    return generate_graph(yaxis_value)

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatterx', 'value'),
    Input('scattery', 'value'))
def update_scatter(scatterx, scattery):
    return generate_scatter(scatterx, scattery)

@app.callback(
    Output('word-cloud', 'figure'),
    Input('Val', 'value'))
def update_wordcloud(val):
    return generate_wordcloud(val)

@app.callback(
    Output('worldmap', 'figure'),
    Input('Val1', 'value'))
def update_worldmap(val):
    return generate_worldmap(val)

if __name__ == '__main__':
    app.run_server(debug=True)
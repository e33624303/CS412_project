import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from data import data_init

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = data_init()

fig = px.bar(df, x="Country", y="Deaths", color="Years", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Data Mining Project
    '''),

    dcc.Graph(
        id='bar-chart',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
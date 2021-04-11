# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('summary.csv')

available_tasks = df['task'].unique()

app.layout = html.Div([
    
    
    dcc.Dropdown(
        id='task',
        options=[{'label': i, 'value': i} for i in available_tasks],
        value='eyegazeall'
    ),
    
    dcc.Graph(id='fd-graphic'),
    dcc.Graph(id='fd_mean-graphic'),
    dcc.Graph(id='std_dvars-graphic'),
    dcc.Graph(id='std_dvars_mean-graphic'),

])

@app.callback(
    Output('fd-graphic', 'figure'),
    Output('fd_mean-graphic', 'figure'),
    Output('std_dvars-graphic', 'figure'),
    Output('std_dvars_mean-graphic', 'figure'),
    Input('task', 'value'))

def update_graph(task_value):
    dff = df[df['task'] == task_value]

    fig_fd = px.strip(dff, x = dff['ses'], y = dff['fd-per'])
    fig_fd_mean = px.strip(dff, x = dff['ses'], y = dff['fd-mean'])

    fig_std_dvar = px.strip(dff, x = dff['ses'], y = dff['std_dvars-per'])
    fig_std_dvar_mean = px.strip(dff, x = dff['ses'], y = dff['std_dvars-mean'])


    #fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
    #                 y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
    #                 hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    #fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')



    return fig_fd, fig_fd_mean, fig_std_dvar, fig_std_dvar_mean


if __name__ == '__main__':
    app.run_server(debug=True)
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# need the requests_pathname_prefix when when running with apache so 
# can find the dash js files
# TODO - how to be able to configure this based on whether running this for
# apache and docker?
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
#   requests_pathname_prefix='/eyegazeqc/')  # for docker
	requests_pathname_prefix='/')  # for testing

df = pd.read_csv('summary.csv')

available_tasks = df['task'].unique()

markdown_text = '''
### Dashboard for eyegaze fmri data quality control

This app was created using Dash for python from [plotly.com](https://dash.plotly.com/)

The qc data were generated using [fmriprep](https://fmriprep.org/en/stable/outputs.html#confounds)

The code is located [here](https://github.com/kelvinlim/mriqc_tools).  The program fmriprep_qc.py
reads in all available *desc-confounds_regressors.tsv files and summarizes them into a summary.csv file.
The summary.csv file is then read by the Dash app.

'''

app.layout = html.Div([
    
    dcc.Markdown(children=markdown_text),

    dcc.Dropdown(
        id='task',
        options=[{'label': i, 'value': i} for i in available_tasks],
        value='eyegazeall'
    ),
    
    dcc.Graph(id='fd-graphic'),
    dcc.Graph(id='fd_mean-graphic'),
    dcc.Graph(id='dvars-graphic'),
    dcc.Graph(id='dvars_mean-graphic'),
    dcc.Graph(id='std_dvars-graphic'),
    dcc.Graph(id='std_dvars_mean-graphic'),

])

@app.callback(
    Output('fd-graphic', 'figure'),
    Output('fd_mean-graphic', 'figure'),
    Output('dvars-graphic', 'figure'),
    Output('dvars_mean-graphic', 'figure'),
    Output('std_dvars-graphic', 'figure'),
    Output('std_dvars_mean-graphic', 'figure'),
    Input('task', 'value'))

def update_graph(task_value):
    dff = df[df['task'] == task_value]

    fig_fd = px.strip(dff, x = dff['ses'], y = dff['fd-per'])
    fig_fd_mean = px.strip(dff, x = dff['ses'], y = dff['fd-mean'])

    fig_dvars = px.strip(dff, x = dff['ses'], y = dff['dvars-per'])
    fig_dvars_mean = px.strip(dff, x = dff['ses'], y = dff['dvars-mean'])

    fig_std_dvars = px.strip(dff, x = dff['ses'], y = dff['std_dvars-per'])
    fig_std_dvars_mean = px.strip(dff, x = dff['ses'], y = dff['std_dvars-mean'])


    #fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
    #                 y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
    #                 hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    #fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')



    return fig_fd, fig_fd_mean,fig_dvars, fig_dvars_mean, fig_std_dvars, fig_std_dvars_mean


if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=5003)

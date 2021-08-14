from datetime import timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

tel = pd.read_csv("azure-data/PdM_telemetry.csv")
tel["datetime_dt"] = pd.to_datetime(tel.datetime)
mach = pd.read_csv("azure-data/PdM_machines.csv")
# [{"label":1, "value":1}]
mach_options = [{"label": i, "value": i}for i in mach.machineID]
default_mach_option = mach_options[0]['value']

min_date = min(tel.datetime_dt)
max_date = max(tel.datetime_dt)
default_end_date = min_date + timedelta(days=2)
print(min_date, max_date, sep="/")
author = "Angel Castillo"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Process control"),
    html.H2(f"By: {author}"),
    html.H3(f"This is a graph"),
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        start_date=min_date,
        end_date=default_end_date
    ),
    dcc.Dropdown(options=mach_options, value=default_mach_option, id="machine-dropdown"),
    dcc.Graph(id="tel-graph")
])


@app.callback(
    Output(component_id='tel-graph', component_property='figure'),
    [Input(component_id='date-picker', component_property='start_date'),
     Input(component_id='date-picker', component_property='end_date'),
     Input(component_id='machine-dropdown', component_property='value')])
def update_output_div(start, end, machine):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    query = """
       datetime_dt > @start and \
       datetime_dt < @end and \
       machineID == @machine \
       """
    filter_tel = tel.query(query)
    fig = go.Figure()

    fig.add_trace(go.Scattergl(x=filter_tel['datetime'], y=filter_tel['volt'],
                        mode='markers',
                        name='markers'))

    fig.add_trace(go.Scattergl(x=filter_tel['datetime'], y=filter_tel['rotate'],
                        mode='lines+markers',
                        name='lines+markers'))

    fig.add_trace(go.Scattergl(x=filter_tel['datetime'], y=filter_tel['pressure'],
                        mode='lines',
                        name='lines'))

    fig.add_trace(go.Scattergl(x=filter_tel['datetime'], y=filter_tel['vibration'],
                        mode='lines+markers',
                        name='lines+markers'))

    # for c in filter_tel.columns[2:]:
    #"volt","rotate","pressure","vibration"

    return fig


app.run_server(debug=True)

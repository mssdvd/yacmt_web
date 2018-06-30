import os

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from sqlalchemy import create_engine

app = dash.Dash()
server = app.server
VALID_USER_PASS = [[os.getenv("USER"), os.getenv("PASS")]]
auth = dash_auth.BasicAuth(app, VALID_USER_PASS)
engine = create_engine(os.getenv("DATABASE_URL"))

DATA = pandas.read_sql("SELECT * FROM reports", engine)

app.layout = html.Div([
    html.H1('YACMT'),
    html.H4('Records'),
    dt.DataTable(
        rows=DATA.to_dict('records'),
        filterable=True,
        sortable=True,
        selected_row_indices=[]),
    html.H5("Velocità max: " + str(DATA["speed"].max())),
    html.H5("Velocità media: " + str(round(DATA["speed"].mean(), 2))),
    dcc.Dropdown(
        id='yaxis-column',
        options=[{
            'label': "Carico del motore",
            'value': 'eng_load'
        }, {
            'label': 'Velocità',
            'value': 'speed'
        }, {
            'label': 'RPM',
            'value': 'eng_rpm'
        }],
        value="eng_load"),
    dcc.Graph(id="time-graph")
])


@app.callback(
    Output("time-graph", "figure"), [
        Input("yaxis-column", "value"),
    ])
def update_time_graph(yaxis_column_value):
    return {
        'data': [go.Scatter(x=DATA['datetime'], y=DATA[yaxis_column_value])],
        'layout':
        go.Layout(
            xaxis={
                'title': "Tempo",
                'type': 'category'
            },
            yaxis={
                'title': yaxis_column_value,
                # 'type': 'line'
            },
            margin={
                'l': 60,
                'b': 100,
                't': 10,
                'r': 0
            },
            hovermode='closest')
    }


app.title = "YACMT"
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
if __name__ == '__main__':
    app.run()

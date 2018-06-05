import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas
import plotly
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine

app = dash.Dash()
engine = create_engine(
    "***REMOVED***"
)

DATA = pandas.read_sql("SELECT * FROM reports", engine)

app.layout = html.Div([
    html.H4('Records'),
    dt.DataTable(
        rows=DATA.to_dict('records'),
        filterable=True,
        sortable=True,
        selected_row_indices=[])
])
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
if __name__ == '__main__':
    app.run_server(debug=True)

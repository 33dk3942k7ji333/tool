import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/reports", name="Reports")

layout = dbc.Container(
    [
        html.H2("Generated Reports", className="mb-4"),
        dbc.Button("Generate New Local Table", id="report-gen-btn", color="warning", className="mb-3"),
        html.Div(id="report-table-container"),
    ],
    fluid=True,
)

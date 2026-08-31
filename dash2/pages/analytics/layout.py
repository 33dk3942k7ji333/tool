import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/analytics", name="Analytics")

layout = dbc.Container(
    [
        html.H2("Performance Analytics", className="mb-4"),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Button("Refresh Chart Data", id="analytics-refresh-btn", color="success", className="mb-3"),
                        dcc.Graph(id="analytics-graph"),
                    ]
                )
            ]
        ),
    ],
    fluid=True,
)

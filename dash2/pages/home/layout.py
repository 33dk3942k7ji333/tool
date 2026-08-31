import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/", name="Home")

layout = dbc.Container(
    [
        html.H2("System Dashboard", className="mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Active Tasks", className="card-title"),
                                    html.H3("1,284", className="text-primary"),
                                ]
                            )
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [html.H5("CPU Usage", className="card-title"), html.H3("42%", className="text-success")]
                            )
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Error Rate", className="card-title"),
                                    html.H3("0.04%", className="text-danger"),
                                ]
                            )
                        ]
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Button("Generate Random Status", id="home-btn", color="primary"),
                        html.Div(id="home-output", className="mt-3"),
                    ]
                )
            ]
        ),
    ],
    fluid=True,
)

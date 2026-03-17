import dash_bootstrap_components as dbc
from components.sidebar import render_sidebar
from dash import dcc, html, page_container
from ids import BaseLayoutIDs


def create_layout():
    return html.Div(
        [
            dcc.Location(id=BaseLayoutIDs.URL),
            render_sidebar(),
            html.Div(
                id=BaseLayoutIDs.CONTENT,
                children=[
                    dbc.Container(
                        children=page_container,
                        className="py-4 px-4 h-100",
                        fluid=True,
                    ),
                    # TODO: 可以在這裡加入全局的 Footer
                ],
                className="content-style",
            ),
        ],
        className="d-flex w-100",
    )

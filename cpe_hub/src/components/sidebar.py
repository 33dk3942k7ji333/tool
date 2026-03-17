import dash_bootstrap_components as dbc
from dash import html
from ids import SidebarIDs


def render_sidebar():
    return html.Div(
        id=SidebarIDs.SIDEBAR_CONTAINER,
        children=[
            html.Div(
                [
                    html.H2(
                        id=SidebarIDs.LOGO,
                        children="DASH",
                        className="display-6 text-primary fw-bold mb-0",
                    ),
                    dbc.Button(
                        id=SidebarIDs.TOGGLE_BUTTON,
                        children=html.I(className="bi bi-list"),
                        outline=True,
                        color="secondary",
                        size="sm",
                    ),
                ],
                className="sidebar-header px-3",
            ),
            html.Hr(className="mx-3 sidebar-divider"),
            dbc.Nav(
                [
                    dbc.NavLink(
                        children=[html.I(className="bi bi-house me-3"), html.Span("Home")],
                        href="/",
                        active="exact",
                        className="nav-item-custom",
                    ),
                    dbc.NavLink(
                        children=[html.I(className="bi bi-folder me-3"), html.Span("Files")],
                        href="/file-manage",
                        active="exact",
                        className="nav-item-custom",
                    ),
                    dbc.NavLink(
                        children=[html.I(className="bi bi-cpu me-3"), html.Span("Service")],
                        href="/service",
                        active="exact",
                        className="nav-item-custom",
                    ),
                ],
                vertical=True,
                pills=True,
                className="px-2",
            ),
            # TODO: 底部可以加入使用者資訊或設定按鈕
        ],
        className="sidebar-style",
    )

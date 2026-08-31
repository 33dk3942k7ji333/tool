import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from dash_bootstrap_components import Button, Card, CardBody, Col, Container, Nav, NavLink, Row

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
)

# 懸浮側邊欄元件
sidebar = html.Div(
    [
        html.Div(className="sidebar-trigger"),
        html.Div(
            className="custom-sidebar p-3 bg-body-tertiary border-end",
            children=[
                # 頂部標題
                html.Div([html.H4("CPE Analyzer", className="fw-bold mb-0 text-primary"), html.Hr()]),
                # 中間頁面選單
                html.Div(
                    className="flex-grow-1",
                    children=[
                        dbc.Nav(
                            [
                                dbc.NavLink(
                                    [html.I(className="bi bi-house-door-fill me-2"), "Home"], href="/", active="exact"
                                ),
                                dbc.NavLink(
                                    [html.I(className="bi bi-bar-chart-line-fill me-2"), "Analytics"],
                                    href="/analytics",
                                    active="exact",
                                ),
                                dbc.NavLink(
                                    [html.I(className="bi bi-file-earmark-text-fill me-2"), "Reports"],
                                    href="/reports",
                                    active="exact",
                                ),
                            ],
                            vertical=True,
                            pills=True,
                        )
                    ],
                ),
                # 底部控制區（Theme 切換、設定、使用者資訊）
                html.Div(
                    [
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        html.I(id="theme-icon", className="bi bi-moon-stars-fill"),
                                        id="theme-toggle-btn",
                                        color="outline-secondary",
                                        size="sm",
                                        className="w-100",
                                    ),
                                    width=4,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        html.I(className="bi bi-gear-fill"),
                                        id="settings-btn",
                                        color="outline-secondary",
                                        size="sm",
                                        className="w-100",
                                        disabled=True,
                                    ),
                                    width=4,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        html.I(className="bi bi-person-circle"),
                                        id="user-btn",
                                        color="outline-secondary",
                                        size="sm",
                                        className="w-100",
                                        disabled=True,
                                    ),
                                    width=4,
                                ),
                            ],
                            className="g-1",
                        ),
                    ]
                ),
            ],
        ),
    ]
)

# 主要 Layout
app.layout = html.Div(
    id="app-container",
    **{"data-bs-theme": "light"},  # Bootstrap 5 原生深淺色切換屬性
    children=[
        dcc.Store(id="theme-store", data="light"),
        sidebar,
        html.Div(className="main-content", children=[dash.page_container]),
    ],
)


# 主題切換 Callback：同時更新 data-bs-theme 屬性與按鈕 Icon
@app.callback(
    Output("app-container", "data-bs-theme"),
    Output("theme-store", "data"),
    Output("theme-icon", "className"),
    Input("theme-toggle-btn", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    if n_clicks % 2 == 1:
        return "dark", "dark", "bi bi-sun-fill"
    return "light", "light", "bi bi-moon-stars-fill"


if __name__ == "__main__":
    app.run(debug=True)

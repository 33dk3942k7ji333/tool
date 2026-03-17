import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.H2("系統概覽", className="fw-bold"),
        html.P("歡迎使用現代化 Dash 管理後台", className="text-muted"),
        # TODO: 增加數據看板元件
    ]
)

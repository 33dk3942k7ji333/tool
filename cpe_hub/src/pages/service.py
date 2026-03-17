import dash
from dash import html

dash.register_page(__name__, path="/service")

layout = html.Div(
    [
        html.H2("服務監控"),
        # TODO: 實作服務狀態列表 (Running/Stopped)
    ]
)

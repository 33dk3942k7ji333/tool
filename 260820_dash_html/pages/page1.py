import dash
from dash import html

dash.register_page(__name__, path="/", name="Sample Page 1")

layout = html.Div(
    children=[
        html.H1("Sample Page 1", style={"color": "#0f172a"}),
        html.P("這是第一個空白頁面範例內容。", style={"color": "#64748b"}),
    ]
)

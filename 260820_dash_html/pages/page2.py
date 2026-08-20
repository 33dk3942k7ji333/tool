import dash
from dash import html

dash.register_page(__name__, path="/page2", name="Sample Page 2")

layout = html.Div(
    children=[
        html.H1("Sample Page 2", style={"color": "#0f172a"}),
        html.P("這是第二個空白頁面範例內容。", style={"color": "#64748b"}),
    ]
)

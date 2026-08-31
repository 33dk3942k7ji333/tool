import random

import plotly.graph_objects as go
from dash import Input, Output, callback


@callback(
    Output("analytics-graph", "figure"),
    Input("analytics-refresh-btn", "n_clicks"),
    Input("theme-store", "data"),  # 監聽主題切換以更新圖表背景
)
def update_analytics_chart(n, theme):
    x_data = [f"Day {i}" for i in range(1, 8)]
    y_data = [random.randint(20, 100) for _ in range(7)]

    template = "plotly_dark" if theme == "dark" else "plotly"

    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, mode="lines+markers", name="Traffic"))
    fig.update_layout(
        title="Weekly Traffic Volume", template=template, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

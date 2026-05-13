import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

app = Dash(__name__)
server = app.server  # 給 Gunicorn/Azure 使用

# 模擬更豐富的資料集
df = pd.DataFrame(
    {
        "Region": ["North", "North", "South", "South", "East", "East", "West", "West"],
        "Product": ["Gadget", "Widget", "Gadget", "Widget", "Gadget", "Widget", "Gadget", "Widget"],
        "Sales": [100, 150, 200, 120, 80, 190, 210, 130],
        "Growth": [5, 10, -2, 8, 3, 12, 15, -5],
    }
)

app.layout = html.Div(
    [
        html.H1("銷售數據視覺化中心", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("選擇產品線："),
                dcc.Dropdown(
                    id="product-dropdown",
                    options=[{"label": i, "value": i} for i in df["Product"].unique()],
                    value="Gadget",
                ),
            ],
            style={"width": "30%", "margin": "20px"},
        ),
        html.Div([dcc.Graph(id="sales-bar-chart"), dcc.Graph(id="growth-scatter-plot")], style={"display": "flex"}),
    ]
)


@app.callback(Output("sales-bar-chart", "figure"), Input("product-dropdown", "value"))
def update_bar_chart(selected_product):
    filtered_df = df[df["Product"] == selected_product]
    fig = px.bar(filtered_df, x="Region", y="Sales", title=f"{selected_product} 各區銷售額")
    return fig


@app.callback(Output("growth-scatter-plot", "figure"), Input("product-dropdown", "value"))
def update_scatter(selected_product):
    filtered_df = df[df["Product"] == selected_product]
    fig = px.scatter(
        filtered_df, x="Sales", y="Growth", color="Region", size="Sales", title=f"{selected_product} 銷售與成長關聯"
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)

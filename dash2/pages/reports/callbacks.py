import random

import dash_bootstrap_components as dbc
from dash import Input, Output, callback


@callback(Output("report-table-container", "children"), Input("report-gen-btn", "n_clicks"))
def generate_report_table(n):
    rows = []
    for i in range(1, 6):
        val = random.randint(100, 999)
        rows.append(html.Tr([html.Td(f"Report-{i}"), html.Td(f"Metric-{val}"), html.Td("Passed")]))

    table = dbc.Table(
        [html.Thead(html.Tr([html.Th("ID"), html.Th("Metric"), html.Th("Status")])), html.Tbody(rows)],
        bordered=True,
        hover=True,
        responsive=True,
        className="mt-3",
    )

    return table

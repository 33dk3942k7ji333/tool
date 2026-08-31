import random

from dash import Input, Output, callback


@callback(
    Output("home-output", "children"),
    Input("home-btn", "n_clicks"),
    prevent_initial_call=True
)
def update_home_status(n):
    status = random.choice(["All systems operational", "Minor latency detected", "Routine maintenance scheduled"])
    return f"System Check #{n}: {status}"    status = random.choice(["All systems operational", "Minor latency detected", "Routine maintenance scheduled"])
    return f"System Check #{n}: {status}"
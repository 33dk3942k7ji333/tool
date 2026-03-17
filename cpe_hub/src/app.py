import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import dash
import dash_bootstrap_components as dbc
from callbacks import register_callbacks
from layout import create_layout

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = create_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)

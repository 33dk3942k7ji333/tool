from dash import Input, Output, State
from ids import SidebarIDs


def register_sidebar_callbacks(app):
    @app.callback(
        [Output(SidebarIDs.SIDEBAR_CONTAINER, "className"), Output("page-content", "className")],
        [Input(SidebarIDs.TOGGLE_BUTTON, "n_clicks")],
        [State(SidebarIDs.SIDEBAR_CONTAINER, "className")],
        prevent_initial_call=True,
    )
    def toggle_sidebar(n, current_class):
        if "collapsed" in current_class:
            return "sidebar-style", "content-style"
        return "sidebar-style collapsed", "content-style expanded"

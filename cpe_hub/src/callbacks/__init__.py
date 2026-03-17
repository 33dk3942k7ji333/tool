from .file_manage_callback import register_file_callbacks
from .sidebar_callback import register_sidebar_callbacks


def register_callbacks(app):
    register_sidebar_callbacks(app)
    register_file_callbacks(app)

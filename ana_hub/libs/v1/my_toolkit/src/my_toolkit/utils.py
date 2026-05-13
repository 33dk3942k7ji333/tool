from my_toolkit.core import get_version


def get_system_report():
    v = get_version()
    return f"System Status: OK | Version: {v}"

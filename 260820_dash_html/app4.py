import os

import dash
import flask
from dash import dcc, html

# 1. 初始化 Dash App 並開啟 multi-page 模式
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.title = "Dash Multi-Page App"

# 指定 HTML 報表存放目錄
REPORTS_DIR = "output_reports"


# 2. 設定 Flask 路由提供 HTML 檔案存取
@app.server.route("/reports/<path:path>")
def serve_reports(path):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    return flask.send_from_directory(REPORTS_DIR, path)


# 3. 整體 UI Layout (Sidebar + Main Content)
app.layout = html.Div(
    style={
        "display": "flex",
        "height": "100vh",
        "fontFamily": "system-ui, -apple-system, sans-serif",
        "backgroundColor": "#f8fafc",
        "margin": "0",
    },
    children=[
        # ── 左側固定 Sidebar ─────────────────────────────────────
        html.Div(
            style={
                "width": "240px",
                "backgroundColor": "#1e293b",
                "color": "#ffffff",
                "padding": "20px 16px",
                "display": "flex",
                "flexDirection": "column",
                "gap": "10px",
                "boxSizing": "border-box",
            },
            children=[
                html.H3("管理系統", style={"margin": "0 0 20px 0", "fontSize": "18px", "color": "#38bdf8"}),
                # 頁面導覽連結
                dcc.Link(
                    "頁面一 (Sample 1)",
                    href="/",
                    className="nav-link",
                    style={"color": "#cbd5e1", "textDecoration": "none", "padding": "8px 12px", "borderRadius": "6px"},
                ),
                dcc.Link(
                    "頁面二 (Sample 2)",
                    href="/page2",
                    className="nav-link",
                    style={"color": "#cbd5e1", "textDecoration": "none", "padding": "8px 12px", "borderRadius": "6px"},
                ),
                dcc.Link(
                    "HTML 報表檢視",
                    href="/reports",
                    className="nav-link",
                    style={"color": "#cbd5e1", "textDecoration": "none", "padding": "8px 12px", "borderRadius": "6px"},
                ),
            ],
        ),
        # ── 右側主要內容呈現區 (自動載入 pages/ 裡對應頁面) ───────────
        html.Div(
            style={"flex": "1", "padding": "24px", "overflowY": "auto", "boxSizing": "border-box"},
            children=[dash.page_container],
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)

import os

import dash
from dash import Input, Output, callback, dcc, html

dash.register_page(__name__, path="/reports", name="HTML 報表檢視")

REPORTS_DIR = "output_reports"


def get_html_files():
    """動態掃描資料夾內所有的 .html 檔案"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
        return []
    files = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]
    files.sort()
    return files


# 頁面二欄式 Layout
layout = html.Div(
    style={"display": "flex", "height": "calc(100vh - 48px)", "gap": "16px", "boxSizing": "border-box"},
    children=[
        # ── 左側：報表選單列表 ─────────────────────────────────
        html.Div(
            style={
                "width": "260px",
                "backgroundColor": "#ffffff",
                "border": "1px solid #e2e8f0",
                "borderRadius": "8px",
                "padding": "16px",
                "display": "flex",
                "flexDirection": "column",
                "gap": "12px",
                "boxSizing": "border-box",
            },
            children=[
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                    children=[
                        html.Span("報表清單", style={"fontWeight": "600", "fontSize": "14px", "color": "#475569"}),
                        html.Button(
                            "重新整理",
                            id="btn-refresh-reports",
                            style={
                                "backgroundColor": "#f1f5f9",
                                "color": "#334155",
                                "border": "1px solid #cbd5e1",
                                "padding": "4px 8px",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                                "fontSize": "12px",
                            },
                        ),
                    ],
                ),
                html.Div(
                    style={"overflowY": "auto", "flex": "1"},
                    children=[
                        dcc.RadioItems(
                            id="selected-report-radio",
                            options=[],
                            value=None,
                            labelStyle={
                                "display": "block",
                                "padding": "8px 12px",
                                "borderRadius": "6px",
                                "marginBottom": "4px",
                                "cursor": "pointer",
                                "fontSize": "13px",
                                "backgroundColor": "#f8fafc",
                                "border": "1px solid #e2e8f0",
                            },
                            inputStyle={"marginRight": "8px"},
                        )
                    ],
                ),
            ],
        ),
        # ── 右側：Iframe 預覽區 ────────────────────────────────
        html.Div(
            style={"flex": "1", "display": "flex", "flexDirection": "column", "gap": "12px", "boxSizing": "border-box"},
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "backgroundColor": "#ffffff",
                        "padding": "10px 16px",
                        "borderRadius": "8px",
                        "border": "1px solid #e2e8f0",
                    },
                    children=[
                        html.Span(
                            id="current-file-label",
                            children="請選擇報表",
                            style={"fontSize": "14px", "color": "#0284c7", "fontWeight": "500"},
                        ),
                        html.A(
                            "全螢幕/新分頁開啟",
                            id="open-new-tab-btn",
                            href="#",
                            target="_blank",
                            style={"color": "#64748b", "fontSize": "13px", "textDecoration": "none"},
                        ),
                    ],
                ),
                html.Iframe(
                    id="report-frame",
                    style={
                        "width": "100%",
                        "flex": "1",
                        "border": "1px solid #e2e8f0",
                        "borderRadius": "8px",
                        "backgroundColor": "#ffffff",
                    },
                ),
            ],
        ),
    ],
)

# ── Callbacks ───────────────────────────────────────────────


# 1. 當點擊「重新整理」或剛載入頁面時更新檔案列表
@callback(
    [Output("selected-report-radio", "options"), Output("selected-report-radio", "value")],
    [Input("btn-refresh-reports", "n_clicks")],
)
def update_report_list(_):
    files = get_html_files()
    if not files:
        return [], None

    options = [{"label": f, "value": f} for f in files]
    return options, files[0]


# 2. 當選取報表時切換 Iframe 畫面與連結
@callback(
    [Output("report-frame", "src"), Output("current-file-label", "children"), Output("open-new-tab-btn", "href")],
    [Input("selected-report-radio", "value")],
)
def display_selected_report(selected_file):
    if not selected_file:
        return "", "目錄內尚無 HTML 報表", "#"

    file_url = f"/reports/{selected_file}"
    return file_url, f"正在預覽：{selected_file}", file_url

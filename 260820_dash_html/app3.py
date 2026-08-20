import os

import dash
from dash import Input, Output, dcc, html

# 1. 建立 Dash App，引入 FontAwesome 圖示與 Inter 字體
external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,  # 雙重防護：允許動態元件與初始空狀態
)
app.title = "機台 KPI 智慧監控中心"

# 指定存放 HTML 報表的資料夾
REPORTS_DIR = "output_reports"


# 2. 開放 Flask 路由以提供 HTML 靜態檔案預覽
@app.server.route("/reports/<path:path>")
def serve_reports(path):
    import flask

    return flask.send_from_directory(REPORTS_DIR, path)


def get_html_files():
    """動態掃描資料夾內所有的 .html 檔案"""
    if not os.path.exists(REPORTS_DIR):
        return []
    files = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]
    files.sort()
    return files


# 3. 現代化 UI Layout (Dark Modern Theme)
app.layout = html.Div(
    style={
        "fontFamily": "'Inter', sans-serif",
        "backgroundColor": "#0f172a",  # Slate 900 質感深灰
        "color": "#f8fafc",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
    },
    children=[
        # ── 頂部導覽列 (Navbar) ──────────────────────────────────
        html.Header(
            style={
                "height": "64px",
                "backgroundColor": "#1e293b",
                "borderBottom": "1px solid #334155",
                "padding": "0 28px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
            },
            children=[
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "12px"},
                    children=[
                        html.I(className="fa-solid fa-microchip", style={"fontSize": "22px", "color": "#38bdf8"}),
                        html.Span(
                            "機台 KPI 智慧監控系統",
                            style={"fontSize": "18px", "fontWeight": "700", "letterSpacing": "0.5px"},
                        ),
                        html.Span(
                            "v2.4 Live",
                            style={
                                "fontSize": "11px",
                                "backgroundColor": "rgba(56, 189, 248, 0.15)",
                                "color": "#38bdf8",
                                "padding": "2px 8px",
                                "borderRadius": "12px",
                                "border": "1px solid rgba(56, 189, 248, 0.3)",
                            },
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "fontSize": "13px",
                        "color": "#94a3b8",
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "16px",
                    },
                    children=[
                        html.Span(
                            [
                                html.I(className="fa-regular fa-clock", style={"marginRight": "6px"}),
                                "自動掃描模式：開啟",
                            ]
                        ),
                        html.Button(
                            id="btn-refresh",
                            children=[
                                html.I(className="fa-solid fa-arrows-rotate", style={"marginRight": "6px"}),
                                "重新整理清單",
                            ],
                            style={
                                "backgroundColor": "#334155",
                                "color": "#f8fafc",
                                "border": "none",
                                "padding": "6px 14px",
                                "borderRadius": "6px",
                                "cursor": "pointer",
                                "fontSize": "12px",
                                "fontWeight": "500",
                                "transition": "0.2s",
                            },
                        ),
                    ],
                ),
            ],
        ),
        # ── 主內容區域：側邊欄 + 預覽視窗 ────────────────────────
        html.Div(
            style={"display": "flex", "flex": "1", "overflow": "hidden"},
            children=[
                # ── 左側：側邊欄 (Sidebar) ─────────────────────────
                html.Aside(
                    style={
                        "width": "320px",
                        "backgroundColor": "#1e293b",
                        "borderRight": "1px solid #334155",
                        "padding": "20px",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "16px",
                    },
                    children=[
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                            children=[
                                html.Span(
                                    "偵測到的機台報表",
                                    style={
                                        "fontSize": "13px",
                                        "fontWeight": "600",
                                        "color": "#94a3b8",
                                        "textTransform": "uppercase",
                                        "letterSpacing": "0.5px",
                                    },
                                ),
                                html.Span(
                                    id="file-count-badge",
                                    children="0 份",
                                    style={
                                        "fontSize": "12px",
                                        "backgroundColor": "#0284c7",
                                        "color": "#ffffff",
                                        "padding": "2px 8px",
                                        "borderRadius": "10px",
                                    },
                                ),
                            ],
                        ),
                        # 固定的 RadioItems 容器，預設在初始 Layout 中即存在，避免 ID Not Found 錯誤
                        html.Div(
                            style={"overflowY": "auto", "flex": "1"},
                            children=[
                                dcc.RadioItems(
                                    id="selected-report-radio",
                                    options=[],
                                    value=None,
                                    labelStyle={
                                        "display": "block",
                                        "backgroundColor": "#0f172a",
                                        "border": "1px solid #334155",
                                        "padding": "12px 16px",
                                        "borderRadius": "8px",
                                        "marginBottom": "8px",
                                        "cursor": "pointer",
                                        "transition": "all 0.2s ease",
                                    },
                                    inputStyle={"marginRight": "10px"},
                                )
                            ],
                        ),
                    ],
                ),
                # ── 右側：主預覽區 (Main Viewer) ──────────────────────
                html.Main(
                    style={
                        "flex": "1",
                        "padding": "20px",
                        "backgroundColor": "#0f172a",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "12px",
                    },
                    children=[
                        # 預覽區標頭資訊
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "backgroundColor": "#1e293b",
                                "padding": "12px 20px",
                                "borderRadius": "8px",
                                "border": "1px solid #334155",
                            },
                            children=[
                                html.Div(
                                    id="current-file-label",
                                    children="請選擇報表",
                                    style={"fontSize": "14px", "fontWeight": "500", "color": "#38bdf8"},
                                ),
                                html.A(
                                    id="open-new-tab-btn",
                                    children=[
                                        html.I(
                                            className="fa-solid fa-arrow-up-right-from-square",
                                            style={"marginRight": "6px"},
                                        ),
                                        "全螢幕開啟",
                                    ],
                                    href="#",
                                    target="_blank",
                                    style={
                                        "color": "#94a3b8",
                                        "textDecoration": "none",
                                        "fontSize": "13px",
                                        "transition": "0.2s",
                                    },
                                ),
                            ],
                        ),
                        # Iframe 內容呈現區
                        html.Iframe(
                            id="report-frame",
                            style={
                                "width": "100%",
                                "flex": "1",
                                "border": "1px solid #334155",
                                "borderRadius": "12px",
                                "backgroundColor": "#ffffff",
                                "boxShadow": "0 10px 25px -5px rgba(0, 0, 0, 0.3)",
                            },
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# 4. Callback: 僅動態更新已存在的 RadioItems options 與 value
@app.callback(
    [
        Output("selected-report-radio", "options"),
        Output("selected-report-radio", "value"),
        Output("file-count-badge", "children"),
    ],
    [Input("btn-refresh", "n_clicks")],
)
def update_sidebar(_):
    files = get_html_files()

    if not files:
        return [], None, "0 份"

    options = []
    for f in files:
        options.append(
            {
                "label": html.Div(
                    style={"display": "inline-flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        html.I(className="fa-regular fa-file-code", style={"color": "#38bdf8"}),
                        html.Span(f, style={"fontSize": "14px", "fontWeight": "500"}),
                    ],
                ),
                "value": f,
            }
        )

    # 回傳選項、預設選取第一個檔案、以及檔案總數標籤
    return options, files[0], f"{len(files)} 份"


# 5. Callback: 當選取項目改變時，切換預覽的 Iframe 與全螢幕開啟連結
@app.callback(
    [
        Output("report-frame", "src"),
        Output("current-file-label", "children"),
        Output("open-new-tab-btn", "href"),
    ],
    [Input("selected-report-radio", "value")],
)
def switch_report(selected_file):
    if not selected_file:
        return "", "尚無選擇的報表", "#"

    file_url = f"/reports/{selected_file}"
    label = [
        html.I(
            className="fa-solid fa-circle-dot", style={"color": "#22c55e", "marginRight": "8px", "fontSize": "10px"}
        ),
        f"正在預覽報表：{selected_file}",
    ]
    return file_url, label, file_url


if __name__ == "__main__":
    app.run(debug=True)

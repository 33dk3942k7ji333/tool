import os

import dash
from dash import dcc, html

app = dash.Dash(__name__, use_pages=True)
REPORTS_DIR = "assets"  # 假設 HTML 檔案都放在 assets/ 資料夾中


def build_menu():
    """動態讀取 assets 資料夾並建立超連結清單"""
    if not os.path.exists(REPORTS_DIR):
        return [html.P("assets 資料夾不存在")]

    html_files = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]

    links = []
    for f in html_files:
        # Dash 會自動將 assets/資料夾映射為根目錄的 /assets/
        file_url = f"/assets/{f}"

        links.append(
            html.Li(
                html.A(
                    f"📄 {f}",
                    href=file_url,
                    target="_blank",  # 在新分頁開啟 HTML
                    style={"textDecoration": "none", "fontSize": "18px", "color": "#007bff"},
                ),
                style={"marginBottom": "8px"},
            )
        )
    return html.Ul(links)


app.layout = html.Div(
    [
        html.H1("自動掃描 HTML 報表選單"),
        html.P("以下連結是自動掃描資料夾後生成的："),
        # 呼叫函式動態生成列表
        build_menu(),
        # 多頁容器
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)

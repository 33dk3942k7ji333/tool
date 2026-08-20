import dash
from dash import dcc, html
from flask import send_from_directory

app = dash.Dash(__name__, use_pages=True)


# 【方法三實作】：利用底層 Flask 伺服器註冊一個路由，直接傳回完整的 HTML 檔案
@app.server.route("/flask-full-html")
def serve_external_html():
    return send_from_directory("assets", "sample.html")


# 主頁面排版與導覽列
app.layout = html.Div(
    [
        html.H1("Dash 呈現外部 HTML 示範應用程式"),
        # 導覽選單
        html.Div(
            [
                dcc.Link("首頁", href="/", style={"margin-right": "15px"}),
                dcc.Link("方法一：Iframe 嵌入", href="/iframe-demo", style={"margin-right": "15px"}),
                dcc.Link("方法二：InnerHTML 解析", href="/inner-html-demo", style={"margin-right": "15px"}),
                html.A("方法三：Flask 全頁跳轉", href="/flask-full-html", target="_blank"),
            ],
            style={"padding": "10px", "background-color": "#eee", "margin-bottom": "20px"},
        ),
        # 子頁面渲染區域
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)

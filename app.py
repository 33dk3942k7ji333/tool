from urllib.parse import unquote

import dash
import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, State, dcc, html

raw_data = [
    {"Name": "config.json", "Path": "/", "Size": "1.2 KB", "Time": "2026-03-10 10:00"},
    {"Name": "README.md", "Path": "/", "Size": "4.5 KB", "Time": "2026-03-11 09:30"},
    {"Name": "main.py", "Path": "/projects/", "Size": "12 KB", "Time": "2026-03-12 14:20"},
    {"Name": "train.csv", "Path": "/projects/data/", "Size": "1.2 MB", "Time": "2026-03-13 08:00"},
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], routes_pathname_prefix="/myhub/")

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Row([dbc.Col(html.H3("MinIO Console", className="my-4 text-primary"), width=12)]),
        # my-4: 垂直方向的外距 (Margin Top & Bottom)，數字 4 代表 1.5rem
        # text-primary: 將文字顏色設定為主題首選色
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id="breadcrumb-nav", className="d-flex align-items-center bg-light p-2 rounded border"),
                    # d-flex: 啟動 Flexbox 佈局，讓子元素可以水平排列
                    # align-items-center: 在 Flex 容器內將子元素垂直居中對齊
                    # bg-light: 設定背景顏色為淺灰色
                    # p-2: 內距 (Padding)，數字 2 代表 0.5rem
                    # rounded: 將容器角落設定為圓角
                    # border: 加上 1px 的淺灰色邊框
                    width=12,
                )
            ],
            className="mb-3",  # mb-3: 下方外距 (Margin Bottom)，數字 3 代表 1rem
        ),
        dbc.Row([dbc.Col(html.Div(id="file-list-container"), width=12)]),
    ],
    fluid=True,  # fluid=True: 讓 Container 寬度佔滿 100% 視窗寬度
)


# ------------------------------------------------------------------------------
# 核心 Callback
# ------------------------------------------------------------------------------
@app.callback(
    [
        Output("breadcrumb-nav", "children"),
        Output("file-list-container", "children"),
    ],
    [Input("url", "hash")],
)
def render_page(current_hash):
    # 1. 解析路徑
    raw_path = unquote(current_hash.replace("#", "")) if current_hash else "/"
    if not raw_path.startswith("/"):
        raw_path = "/" + raw_path

    # --- 關鍵邏輯：判斷是「目錄」還是「選取檔案」 ---
    is_file_selected = not raw_path.endswith("/") and raw_path != "/"

    if is_file_selected:
        # 如果選取了檔案，Table 顯示的資料路徑應該是「該檔案所在的資料夾」
        # 例如 /projects/main.py -> 抓取 /projects/ 的資料
        data_lookup_path = raw_path.rsplit("/", 1)[0] + "/"
        selected_filename = raw_path.rsplit("/", 1)[1]
    else:
        # 如果是目錄，正常顯示
        data_lookup_path = raw_path
        selected_filename = None

    # 2. 資料篩選
    display_items = []
    found_subfolders = set()
    for item in raw_data:
        if item["Path"] == data_lookup_path:
            display_items.append({"name": item["Name"], "type": "file", "size": item["Size"], "time": item["Time"]})
        elif item["Path"].startswith(data_lookup_path):
            relative = item["Path"][len(data_lookup_path) :]
            if relative:
                sub = relative.split("/")[0]
                if sub and sub not in found_subfolders:
                    display_items.append({"name": sub, "type": "folder", "size": "--", "time": "--"})
                    found_subfolders.add(sub)

    display_items.sort(key=lambda x: (x["type"] != "folder", x["name"]))

    # 3. 建立表格內容
    rows = []
    for item in display_items:
        # 判斷此行是否為目前選取的檔案，若是則加一個背景色提示
        is_row_selected = item["type"] == "file" and item["name"] == selected_filename
        row_style = {"backgroundColor": "#ff0000"} if is_row_selected else {}

        if item["type"] == "folder":
            name_cell = html.Td(
                html.A(
                    f"📁 {item['name']}",
                    href=f"#{data_lookup_path}{item['name']}/",
                    style={"textDecoration": "none", "fontWeight": "bold"},
                )
            )
        else:
            # 點擊檔案名稱會更新 URL (但不加斜線)，觸發麵包屑更新
            name_cell = html.Td(
                html.A(
                    f"📄 {item['name']}",
                    href=f"#{data_lookup_path}{item['name']}",
                    style={
                        "textDecoration": "none",
                        "color": "inherit",
                        "cursor": "text",
                    },
                )
            )

        rows.append(html.Tr([name_cell, html.Td(item["size"]), html.Td(item["time"])], style=row_style))

    table = dbc.Table(
        [html.Thead(html.Tr([html.Th("Name"), html.Th("Size"), html.Th("Last Modified")])), html.Tbody(rows)],
        hover=True,
        style={"userSelect": "text"},
    )

    # 4. 建立麵包屑 (包含檔案名稱)
    path_parts = [p for p in raw_path.split("/") if p]
    bc_elements = [html.A("Buckets", href="#/", style={"textDecoration": "none"})]

    temp_path = "/"
    for i, p in enumerate(path_parts):
        # 判斷是否為最後一個元素 (可能是檔案)
        is_last = i == len(path_parts) - 1
        # 如果是目錄則加斜線，如果是檔案則不加
        if is_last and is_file_selected:
            this_path = temp_path + p
        else:
            this_path = temp_path + p + "/"
            temp_path = this_path

        bc_elements.append(html.Span(" / ", className="mx-2 text-muted"))
        bc_elements.append(html.A(p, href=f"#{this_path}", style={"textDecoration": "none"}))

    if len(bc_elements) > 1:
        bc_elements[-1].style.update({"color": "#6c757d", "pointerEvents": "none"})

    return bc_elements, table


if __name__ == "__main__":
    app.run(debug=True)

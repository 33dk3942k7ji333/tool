from urllib.parse import unquote

import dash_bootstrap_components as dbc
from dash import Input, Output, html
from data import raw_data
from ids import BaseLayoutIDs, FileManageIDs

# 將資料宣告在此或從外部導入


def register_file_callbacks(app):
    @app.callback(
        [
            Output(FileManageIDs.BREADCRUMB, "children"),
            Output(FileManageIDs.LIST_CONTAINER, "children"),
        ],
        [Input(BaseLayoutIDs.URL, "hash")],
    )
    def render_file_manager(current_hash):
        # 1. 解析路徑
        raw_path = unquote(current_hash.replace("#", "")) if current_hash else "/"
        if not raw_path.startswith("/"):
            raw_path = "/" + raw_path

        is_file_selected = not raw_path.endswith("/") and raw_path != "/"

        if is_file_selected:
            data_lookup_path = raw_path.rsplit("/", 1)[0] + "/"
            selected_filename = raw_path.rsplit("/", 1)[1]
        else:
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
            is_row_selected = item["type"] == "file" and item["name"] == selected_filename
            # 使用更現代的顏色提示，例如淺藍色
            row_style = {"backgroundColor": "#e7f1ff"} if is_row_selected else {}

            if item["type"] == "folder":
                icon = html.I(className="bi bi-folder-fill me-2 text-warning")
                link_href = f"#/{data_lookup_path.strip('/')}/{item['name']}/".replace("//", "/")
                name_cell = html.Td(
                    html.A([icon, item["name"]], href=link_href, className="text-decoration-none fw-bold")
                )
            else:
                icon = html.I(className="bi bi-file-earmark-text me-2 text-secondary")
                link_href = f"#/{data_lookup_path.strip('/')}/{item['name']}".replace("//", "/")
                name_cell = html.Td(
                    html.A([icon, item["name"]], href=link_href, className="text-decoration-none text-dark")
                )

            rows.append(html.Tr([name_cell, html.Td(item["size"]), html.Td(item["time"])], style=row_style))

        table = dbc.Table(
            [html.Thead(html.Tr([html.Th("Name"), html.Th("Size"), html.Th("Last Modified")])), html.Tbody(rows)],
            hover=True,
            responsive=True,  # 增加響應式支援
            className="mb-0",
        )

        # 4. 建立麵包屑
        path_parts = [p for p in raw_path.split("/") if p]
        bc_elements = []
        bc_elements.append(html.A("Root", href="#/", className="text-decoration-none"))

        temp_path = "/"
        for i, p in enumerate(path_parts):
            is_last = i == len(path_parts) - 1
            if is_last and is_file_selected:
                this_path = temp_path + p
            else:
                this_path = temp_path + p + "/"
                temp_path = this_path

            bc_elements.append(html.Span("/", className="mx-2 text-muted"))
            bc_elements.append(html.A(p, href=f"#{this_path}", className="text-decoration-none"))

        return bc_elements, table

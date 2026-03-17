import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from ids import FileManageIDs

# 註冊頁面，對應到 /file-manage 路由
dash.register_page(__name__, path="/file-manage")


def create_layout():
    """
    使用 function 形式定義 layout，確保每次頁面重載都能獲取最新狀態。
    """
    return dbc.Container(
        [
            dcc.Download(id=FileManageIDs.DOWNLOAD_COMPONENT),
            html.Div(dbc.Checkbox(id=FileManageIDs.SELECT_ALL, value=False), style={"display": "none"}),
            # 頁面標題
            dbc.Row(
                [
                    dbc.Col(
                        html.H3(
                            [html.I(className="bi bi-folder2-open me-2"), "檔案管理系統"],
                            className="my-4 text-primary fw-bold",
                        ),
                        width=12,
                    )
                ]
            ),
            # 工具列：麵包屑 (左) + 按鈕群組 (右)
            dbc.Row(
                [
                    # 麵包屑導航容器
                    dbc.Col(
                        html.Div(
                            id=FileManageIDs.BREADCRUMB,
                            className="d-flex align-items-center bg-white p-2 rounded border shadow-sm",
                            style={"minHeight": "50px"},
                        ),
                        lg=7,
                        md=12,
                        className="mb-2",
                    ),
                    # 按鈕群組
                    dbc.Col(
                        html.Div(
                            [
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            [html.I(className="bi bi-cloud-upload me-2"), "上傳"],
                                            id=FileManageIDs.BTN_UPLOAD,
                                            color="primary",
                                            outline=False,
                                        ),
                                        dbc.Button(
                                            [html.I(className="bi bi-cloud-download me-2"), "下載"],
                                            id=FileManageIDs.BTN_DOWNLOAD,
                                            color="success",
                                            outline=False,
                                        ),
                                        dbc.Button(
                                            [html.I(className="bi bi-trash me-2"), "刪除"],
                                            id=FileManageIDs.BTN_DELETE,
                                            color="danger",
                                            outline=False,
                                        ),
                                        dbc.Button(
                                            [html.I(className="bi bi-arrow-clockwise me-2"), "更新"],
                                            id=FileManageIDs.BTN_REFRESH,
                                            color="info",
                                            className="text-white",
                                        ),
                                    ],
                                    className="shadow-sm",
                                )
                            ],
                            className="d-flex justify-content-lg-end justify-content-start mb-2",
                        ),
                        lg=5,
                        md=12,
                    ),
                ],
                className="mb-3 align-items-center",
            ),
            # 檔案列表主要區域
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                # 這個 Div 會被 file_callback.py 填入 dbc.Table
                                html.Div(
                                    [html.Div(dbc.Spinner(color="primary"), className="text-center py-5")],
                                    id=FileManageIDs.LIST_CONTAINER,
                                )
                            ),
                            className="shadow-sm border-0",
                        ),
                        width=12,
                    )
                ]
            ),
            # 預留一個 Modal 用於上傳檔案 (選配)
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("上傳檔案")),
                    dbc.ModalBody("這裡之後可以放置 dcc.Upload 元件..."),
                    dbc.ModalFooter(dbc.Button("關閉", id="close-upload-modal", className="ms-auto", n_clicks=0)),
                ],
                id="upload-modal",
                is_open=False,
            ),
        ],
        fluid=True,
        className="px-4",
    )


layout = create_layout

import os

from jinja2 import Template

# =========================================================
# 1. 現代化 SVG 微圖表繪製器 (微張力趨勢圖 + 柱狀圖)
# =========================================================


def generate_modern_svg_line_chart():
    """現代化 Glow 效果折線圖 (內嵌 SVG, 支援 CSS 漸層)"""
    return """
    <svg width="100%" height="240" viewBox="0 0 500 240" xmlns="http://www.w3.org/2000/svg" style="overflow: visible;">
        <defs>
            <!-- 折線下方陰影漸層 -->
            <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3"/>
                <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.0"/>
            </linearGradient>
            <!-- 線條鮮豔漸層 -->
            <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#60a5fa"/>
                <stop offset="100%" stop-color="#2563eb"/>
            </linearGradient>
        </defs>

        <!-- 背景輔助線 -->
        <line x1="0" y1="40" x2="500" y2="40" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4"/>
        <line x1="0" y1="100" x2="500" y2="100" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4"/>
        <line x1="0" y1="160" x2="500" y2="160" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4"/>

        <!-- 漸層填充區域 -->
        <polygon fill="url(#areaGradient)" points="20,160 90,110 160,130 230,60 300,80 370,40 480,70 480,200 20,200" />

        <!-- 主趨勢線 -->
        <polyline fill="none" stroke="url(#lineGradient)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"
            points="20,160 90,110 160,130 230,60 300,80 370,40 480,70" />

        <!-- 數據亮點點位 -->
        <circle cx="230" cy="60" r="5" fill="#ffffff" stroke="#2563eb" stroke-width="3"/>
        <circle cx="370" cy="40" r="6" fill="#2563eb" stroke="#ffffff" stroke-width="2"/>

        <!-- X 軸日期標籤 -->
        <text x="20" y="225" font-size="12" fill="#94a3b8" font-weight="500">08/14</text>
        <text x="90" y="225" font-size="12" fill="#94a3b8" font-weight="500">08/15</text>
        <text x="160" y="225" font-size="12" fill="#94a3b8" font-weight="500">08/16</text>
        <text x="230" y="225" font-size="12" fill="#94a3b8" font-weight="500">08/17</text>
        <text x="300" y="225" font-size="12" fill="#94a3b8" font-weight="500">08/18</text>
        <text x="370" y="225" font-size="12" fill="#3b82f6" font-weight="700">08/19</text>
        <text x="480" y="225" font-size="12" fill="#94a3b8" font-weight="500">今日</text>
    </svg>
    """


# 模擬機台測試資料
machines_data = [
    {
        "id": "EQP-101",
        "name": "SMT 高速貼片機 Alpha",
        "category": "表面貼裝設備",
        "location": "竹南廠 - Line A1",
        "operator": "張小明 (ID: 8821)",
        "status": "RUNNING",
        "status_label": "正常運轉中",
        "status_theme": "success",  # success, warning, danger
        "oee": "91.8%",
        "kpis": [
            {"name": "整體設備效率 (OEE)", "value": "91.8%", "target": "85.0%", "trend": "+2.4%", "is_up": True},
            {"name": "時間稼動率 (Availability)", "value": "96.2%", "target": "90.0%", "trend": "+0.8%", "is_up": True},
            {"name": "性能稼動率 (Performance)", "value": "96.0%", "target": "95.0%", "trend": "-0.5%", "is_up": False},
            {"name": "品質良品率 (Quality)", "value": "99.4%", "target": "98.5%", "trend": "+0.1%", "is_up": True},
        ],
        "chart_svg": generate_modern_svg_line_chart(),
    },
    {
        "id": "EQP-102",
        "name": "氮氣回焊爐 Beta",
        "category": "熱處理設備",
        "location": "竹南廠 - Line A1",
        "operator": "李大華 (ID: 7412)",
        "status": "WARNING",
        "status_label": "溫控微幅異常",
        "status_theme": "warning",
        "oee": "78.4%",
        "kpis": [
            {"name": "整體設備效率 (OEE)", "value": "78.4%", "target": "85.0%", "trend": "-5.2%", "is_up": False},
            {
                "name": "時間稼動率 (Availability)",
                "value": "82.1%",
                "target": "90.0%",
                "trend": "-4.1%",
                "is_up": False,
            },
            {"name": "性能稼動率 (Performance)", "value": "96.5%", "target": "95.0%", "trend": "+1.2%", "is_up": True},
            {
                "name": "品質良品率 (Quality)",
                "value": "99.1%",
                "target": "98.5%",
                "status": "達標",
                "trend": "0.0%",
                "is_up": True,
            },
        ],
        "chart_svg": generate_modern_svg_line_chart(),
    },
]

# =========================================================
# 2. 現代化 CSS Dashboard 模板
# =========================================================

modern_html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ machine.id }} - 現代化 KPI 控制台</title>
    <!-- 引入 Inter 現代字體 與 FontAwesome 圖標 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-main: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            
            /* 狀態色彩 */
            --primary: #3b82f6;
            --primary-light: #eff6ff;
            --success: #10b981;
            --success-light: #ecfdf5;
            --warning: #f59e0b;
            --warning-light: #fffbeb;
            --danger: #ef4444;
            --danger-light: #fef2f2;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-primary);
            padding: 24px;
            display: flex;
            justify-content: center;
        }

        .dashboard-container {
            width: 100%;
            max-width: 1100px;
        }

        /* 頂部 Header Card */
        .header-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 24px;
        }

        .header-title-group h1 {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-meta {
            display: flex;
            gap: 20px;
            margin-top: 8px;
            font-size: 13px;
            color: var(--text-secondary);
        }

        .header-meta span {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Status Badges */
        .badge {
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .badge-success { background: var(--success-light); color: var(--success); }
        .badge-warning { background: var(--warning-light); color: var(--warning); }
        .badge-danger { background: var(--danger-light); color: var(--danger); }
        
        .badge-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: currentColor;
        }

        /* KPI Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }

        .kpi-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        }

        .kpi-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 500;
        }

        .kpi-value-group {
            margin-top: 12px;
            display: flex;
            align-items: baseline;
            justify-content: space-between;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .kpi-trend {
            font-size: 12px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 6px;
        }
        .trend-up { background: var(--success-light); color: var(--success); }
        .trend-down { background: var(--danger-light); color: var(--danger); }

        .kpi-target {
            margin-top: 8px;
            font-size: 12px;
            color: var(--text-secondary);
        }

        /* 主圖表與內容區塊 */
        .content-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }

        @media (max-width: 868px) {
            .content-grid { grid-template-columns: 1fr; }
        }

        .main-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .card-header h2 {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
        }

        /* 資訊列表特化 */
        .info-list {
            list-style: none;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid var(--border-color);
            font-size: 14px;
        }

        .info-item:last-child {
            border-bottom: none;
        }

        .info-label {
            color: var(--text-secondary);
        }

        .info-val {
            font-weight: 600;
            color: var(--text-primary);
        }

        /* 頁尾資訊 */
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 12px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>

<div class="dashboard-container">

    <!-- 1. 頂部機台抬頭 -->
    <div class="header-card">
        <div class="header-title-group">
            <h1><i class="fa-solid fa-microchip" style="color: var(--primary);"></i> {{ machine.name }}</h1>
            <div class="header-meta">
                <span><i class="fa-regular fa-id-badge"></i> {{ machine.id }}</span>
                <span><i class="fa-solid fa-location-dot"></i> {{ machine.location }}</span>
                <span><i class="fa-regular fa-folder"></i> {{ machine.category }}</span>
            </div>
        </div>
        <div>
            <span class="badge badge-{{ machine.status_theme }}">
                <span class="badge-dot"></span> {{ machine.status_label }}
            </span>
        </div>
    </div>

    <!-- 2. 4格 KPI 數據特化卡片 -->
    <div class="kpi-grid">
        {% for kpi in machine.kpis %}
        <div class="kpi-card">
            <div class="kpi-top">
                <span>{{ kpi.name }}</span>
                <i class="fa-solid fa-chart-line" style="opacity:0.4;"></i>
            </div>
            <div class="kpi-value-group">
                <div class="kpi-value">{{ kpi.value }}</div>
                <div class="kpi-trend {{ 'trend-up' if kpi.is_up else 'trend-down' }}">
                    <i class="fa-solid {{ 'fa-arrow-up' if kpi.is_up else 'fa-arrow-down' }}"></i> {{ kpi.trend }}
                </div>
            </div>
            <div class="kpi-target">目標門檻值：{{ kpi.target }}</div>
        </div>
        {% endfor %}
    </div>

    <!-- 3. 主內容區域：趨勢圖表 + 系統即時細節 -->
    <div class="content-grid">
        <!-- 左側：近 7 日趨勢圖表 -->
        <div class="main-card">
            <div class="card-header">
                <h2>📈 近 7 日 OEE 綜合指標監控</h2>
                <span style="font-size: 12px; color: var(--text-secondary);">即時數據更新</span>
            </div>
            <div>
                {{ machine.chart_svg | safe }}
            </div>
        </div>

        <!-- 右側：機台監控日誌/負責人 -->
        <div class="main-card">
            <div class="card-header">
                <h2>⚙️ 運轉環境細節</h2>
            </div>
            <ul class="info-list">
                <li class="info-item">
                    <span class="info-label">目前值班工程師</span>
                    <span class="info-val">{{ machine.operator }}</span>
                </li>
                <li class="info-item">
                    <span class="info-label">通訊協定狀態</span>
                    <span class="info-val" style="color: var(--success);"><i class="fa-solid fa-link"></i> SECS/GEM 連線</span>
                </li>
                <li class="info-item">
                    <span class="info-label">上次預防保養 (PM)</span>
                    <span class="info-val">2026-08-01</span>
                </li>
                <li class="info-item">
                    <span class="info-label">數據擷取頻率</span>
                    <span class="info-val">1.0 秒 / 次</span>
                </li>
            </ul>
        </div>
    </div>

    <div class="footer">
        系統自動生成時間：2026-08-20 23:35 | 數據來源：Smart Factory IIoT API
    </div>

</div>

</body>
</html>
"""

# =========================================================
# 3. 批次生成檔案
# =========================================================


def main():
    output_dir = "output_reports"
    os.makedirs(output_dir, exist_ok=True)
    template = Template(modern_html_template)

    for machine in machines_data:
        rendered_html = template.render(machine=machine)
        filename = f"{machine['id']}_KPI_Report.html"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        print(f"✨ 現代化報表已生成：{file_path}")


if __name__ == "__main__":
    main()

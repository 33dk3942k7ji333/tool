import os

from jinja2 import Template

# =========================================================
# 1. 離線資料與圖表產生器 (Offline Data)
# =========================================================


def generate_offline_svg_chart(machine_id, color="#007bff"):
    """生成離線可用的 SVG 折線圖 (無需外部圖檔/網路)"""
    return f'''
    <svg width="100%" height="220" viewBox="0 0 500 220" xmlns="http://www.w3.org/2000/svg" style="background:#fdfdfd; border-radius:6px; border:1px solid #e2e8f0;">
        <!-- 背景網格線 -->
        <line x1="50" y1="30" x2="470" y2="30" stroke="#edf2f7" stroke-width="1"/>
        <line x1="50" y1="80" x2="470" y2="80" stroke="#edf2f7" stroke-width="1"/>
        <line x1="50" y1="130" x2="470" y2="130" stroke="#edf2f7" stroke-width="1"/>
        <line x1="50" y1="180" x2="470" y2="180" stroke="#e2e8f0" stroke-width="1.5"/>
        
        <!-- Y軸標籤 -->
        <text x="40" y="35" font-size="10" fill="#a0aec0" text-anchor="end">100%</text>
        <text x="40" y="85" font-size="10" fill="#a0aec0" text-anchor="end">50%</text>
        <text x="40" y="135" font-size="10" fill="#a0aec0" text-anchor="end">0%</text>
        
        <!-- 趨勢數據折線 -->
        <polyline fill="none" stroke="{color}" stroke-width="3" points="
            60,120 120,70 180,90 240,40 300,60 360,35 420,50
        " />
        
        <!-- 折線數據點 -->
        <circle cx="60" cy="120" r="4" fill="{color}"/>
        <circle cx="120" cy="70" r="4" fill="{color}"/>
        <circle cx="180" cy="90" r="4" fill="{color}"/>
        <circle cx="240" cy="40" r="4" fill="{color}"/>
        <circle cx="300" cy="60" r="4" fill="{color}"/>
        <circle cx="360" cy="35" r="4" fill="{color}"/>
        <circle cx="420" cy="50" r="4" fill="{color}"/>
        
        <!-- X軸標籤 -->
        <text x="60" y="200" font-size="11" fill="#718096" text-anchor="middle">Mon</text>
        <text x="120" y="200" font-size="11" fill="#718096" text-anchor="middle">Tue</text>
        <text x="180" y="200" font-size="11" fill="#718096" text-anchor="middle">Wed</text>
        <text x="240" y="200" font-size="11" fill="#718096" text-anchor="middle">Thu</text>
        <text x="300" y="200" font-size="11" fill="#718096" text-anchor="middle">Fri</text>
        <text x="360" y="200" font-size="11" fill="#718096" text-anchor="middle">Sat</text>
        <text x="420" y="200" font-size="11" fill="#718096" text-anchor="middle">Sun</text>
    </svg>
    '''


# 機台資料與對應的 KPI / 圖表清單
machines_data = [
    {
        "id": "EQP-101",
        "name": "Machine Alpha (貼片機)",
        "location": "廠區 A - Line 1",
        "status": "運作中",
        "status_color": "#28a745",
        "kpis": [
            {"name": "整體設備效率 (OEE)", "value": "88.5%", "target": "85.0%", "status": "達標"},
            {"name": "稼動率 (Availability)", "value": "94.2%", "target": "90.0%", "status": "達標"},
            {"name": "良品率 (Quality)", "value": "99.1%", "target": "98.5%", "status": "達標"},
            {"name": "平均故障間隔 (MTBF)", "value": "120 hrs", "target": "100 hrs", "status": "達標"},
        ],
        "chart_svg": generate_offline_svg_chart("EQP-101", "#007bff"),
        # 若有本地圖片檔案，也可改用: "image_path": "images/eqp101_chart.png"
    },
    {
        "id": "EQP-102",
        "name": "Machine Beta (迴焊爐)",
        "location": "廠區 A - Line 1",
        "status": "警告/維護中",
        "status_color": "#ffc107",
        "kpis": [
            {"name": "整體設備效率 (OEE)", "value": "76.3%", "target": "85.0%", "status": "未達標"},
            {"name": "稼動率 (Availability)", "value": "81.0%", "target": "90.0%", "status": "未達標"},
            {"name": "良品率 (Quality)", "value": "98.7%", "target": "98.5%", "status": "達標"},
            {"name": "平均修復時間 (MTTR)", "value": "2.5 hrs", "target": "< 2.0 hrs", "status": "警示"},
        ],
        "chart_svg": generate_offline_svg_chart("EQP-102", "#dc3545"),
    },
    {
        "id": "EQP-201",
        "name": "Machine Gamma (AOI 光學檢測)",
        "location": "廠區 B - Line 2",
        "status": "運作中",
        "status_color": "#28a745",
        "kpis": [
            {"name": "整體設備效率 (OEE)", "value": "92.1%", "target": "85.0%", "status": "達標"},
            {"name": "稼動率 (Availability)", "value": "96.5%", "target": "90.0%", "status": "達標"},
            {"name": "良品率 (Quality)", "value": "99.8%", "target": "98.5%", "status": "達標"},
            {"name": "誤判率 (False Alarm)", "value": "0.12%", "target": "< 0.20%", "status": "達標"},
        ],
        "chart_svg": generate_offline_svg_chart("EQP-201", "#28a745"),
    },
]

# =========================================================
# 2. Jinja2 HTML 報本範本
# =========================================================

html_template_str = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ machine.name }} - KPI 效能報表</title>
    <style>
        * {
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        }
        body {
            background-color: #f4f6f9;
            color: #333;
            margin: 0;
            padding: 30px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 30px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            color: #1a202c;
        }
        .header .meta {
            font-size: 14px;
            color: #718096;
            margin-top: 5px;
        }
        .status-badge {
            padding: 6px 14px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        
        /* KPI 卡片 */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .kpi-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 15px;
        }
        .kpi-name {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 8px;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: bold;
            color: #0f172a;
        }
        .kpi-target {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 4px;
        }
        
        /* 區塊標題與圖表 */
        .section-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #2d3748;
        }
        .chart-box {
            margin-bottom: 30px;
        }
        
        .footer {
            text-align: center;
            font-size: 12px;
            color: #a0aec0;
            margin-top: 20px;
            border-top: 1px solid #edf2f7;
            padding-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 標頭區塊 -->
        <div class="header">
            <div>
                <h1>{{ machine.name }}</h1>
                <div class="meta">編號：{{ machine.id }} | 位置：{{ machine.location }}</div>
            </div>
            <div class="status-badge" style="background-color: {{ machine.status_color }};">
                {{ machine.status }}
            </div>
        </div>

        <!-- KPI 卡片列表 -->
        <div class="section-title">📊 關鍵效能指標 (KPI)</div>
        <div class="kpi-grid">
            {% for kpi in machine.kpis %}
            <div class="kpi-card">
                <div class="kpi-name">{{ kpi.name }}</div>
                <div class="kpi-value">{{ kpi.value }}</div>
                <div class="kpi-target">目標值：{{ kpi.target }} ({{ kpi.status }})</div>
            </div>
            {% endfor %}
        </div>

        <!-- 趨勢圖表 -->
        <div class="chart-box">
            <div class="section-title">📈 近 7 日效能趨勢圖</div>
            {% if machine.chart_svg %}
                <!-- 內嵌 SVG 圖表 -->
                {{ machine.chart_svg | safe }}
            {% elif machine.image_path %}
                <!-- 本地圖片 -->
                <img src="{{ machine.image_path }}" alt="KPI Chart" style="width:100%; border-radius:6px;">
            {% endif %}
        </div>

        <!-- 頁尾 -->
        <div class="footer">
            本報表為系統自動生成之獨立 HTML 檔案
        </div>
    </div>
</body>
</html>
"""

# =========================================================
# 3. 執行批次生成邏輯
# =========================================================


def main():
    output_dir = "output_reports"
    os.makedirs(output_dir, exist_ok=True)

    template = Template(html_template_str)

    print(f"開始批次生成機台 HTML 報表...\n")

    for machine in machines_data:
        # 渲染 HTML 內容
        rendered_html = template.render(machine=machine)

        # 輸出檔案名稱： output_reports/EQP-101_KPI_Report.html
        filename = f"{machine['id']}_KPI_Report.html"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        print(f"✅ 已成功生成: {file_path}")

    print("\n完成！打開 `output_reports` 資料夾，雙擊檔案即可離線查看。")


if __name__ == "__main__":
    main()

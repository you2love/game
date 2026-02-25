#!/usr/bin/env python3
import os
import re

# More company data
COMPANY_DATA = {
    "lilith.html": {
        "title": "莉莉丝",
        "revenue": [45, 85, 120, 145, 155, 158, 160],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [("海外", 85, "#0891b2"), ("国内", 15, "#7c3aed")],
        "products": [
            ("万国觉醒", 40),
            ("剑与远征", 30),
            ("剑与远征:启程", 20),
            ("其他", 10),
        ],
        "timeline": [
            ("2013", "成立", "创业起步"),
            ("2019", "剑与远征", "放置类爆发"),
            ("2020", "万国觉醒", "SLG全球突破"),
            ("2024", "剑与远征:启程", "续作发布"),
        ],
        "flowchart": """flowchart TB
    A[莉莉丝] --> B[自研产品]
    A --> C[全球发行]
    A --> D[投资布局]
    
    B --> B1[万国觉醒]
    B --> B2[剑与远征]
    B --> B3[剑与远征:启程]
    B --> B4[战火勋章]
    
    C --> C1[欧美市场]
    C --> C2[日韩市场]
    C --> C3[东南亚]
    
    D --> D1[游戏工作室]
    D --> D2[技术公司]
    
    style A fill:#0891b2,color:#fff
    style B fill:#7c3aed,color:#fff
    style C fill:#db2777,color:#fff
    style D fill:#059669,color:#fff""",
    },
    "hypergryph.html": {
        "title": "鹰角网络",
        "revenue": [30, 55, 85, 110, 125, 132, 135],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [("海外", 55, "#0891b2"), ("国内", 45, "#7c3aed")],
        "products": [("明日方舟", 75), ("终末地", 15), ("其他", 10)],
        "timeline": [
            ("2017", "成立", "创业起步"),
            ("2019", "明日方舟上线", "二次元爆款"),
            ("2023", "终末地", "新品发布"),
            ("2024", "明日方舟:终末地", "IP延伸"),
        ],
        "flowchart": """flowchart TB
    A[鹰角网络] --> B[明日方舟]
    A --> C[终末地]
    A --> D[IP衍生]
    
    B --> B1[游戏本体]
    B --> B2[动画]
    B --> B3[漫画]
    
    C --> C1[游戏本体]
    C --> C2[周边]
    
    D --> D1[联名合作]
    D --> D2[线下活动]
    
    style A fill:#0891b2,color:#fff
    style B fill:#7c3aed,color:#fff
    style C fill:#db2777,color:#fff
    style D fill:#059669,color:#fff""",
    },
    "bilibili.html": {
        "title": "哔哩哔哩游戏",
        "revenue": [80, 120, 95, 110, 125, 135, 140],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [
            ("联运", 50, "#0891b2"),
            ("自研", 30, "#7c3aed"),
            ("发行", 20, "#db2777"),
        ],
        "products": [("FGO", 25), ("碧蓝航线", 20), ("公主连结", 15), ("其他", 40)],
        "timeline": [
            ("2014", "游戏联运", "开始游戏业务"),
            ("2016", "独家代理", "FGO国服"),
            ("2019", "自研游戏", "开始自研"),
            ("2023", "海外发行", "全球化布局"),
        ],
        "flowchart": """flowchart TB
    A[哔哩哔哩游戏] --> B[游戏联运]
    A --> C[独家代理]
    A --> D[自研产品]
    
    B --> B1[FGO]
    B --> B2[碧蓝航线]
    B --> B3[公主连结]
    
    C --> C1[独家代理]
    C --> C2[国服首发]
    
    D --> D1[游戏开发]
    D --> D2[发行运营]
    
    style A fill:#0891b2,color:#fff
    style B fill:#7c3aed,color:#fff
    style C fill:#db2777,color:#fff
    style D fill:#059669,color:#fff""",
    },
    "perfectworld.html": {
        "title": "完美世界",
        "revenue": [120, 145, 125, 140, 155, 162, 165],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [
            ("手游", 45, "#0891b2"),
            ("端游", 40, "#7c3aed"),
            ("主机", 15, "#db2777"),
        ],
        "products": [("完美世界", 30), ("诛仙", 25), ("女神联盟", 20), ("其他", 25)],
        "timeline": [
            ("2004", "完美世界", "端游起步"),
            ("2013", "手游转型", "移动化"),
            ("2018", "主机游戏", "STEAM布局"),
            ("2022", "电竞布局", "多元化发展"),
        ],
        "flowchart": """flowchart TB
    A[完美世界] --> B[端游]
    A --> C[手游]
    A --> D[主机游戏]
    
    B --> B1[完美世界]
    B --> B2[诛仙]
    B --> B3[武林外传]
    
    C --> C1[诛仙手游]
    C --> C2[完美世界手游]
    
    D --> D1[主机研发]
    D --> D2[Steam发行]
    
    style A fill:#0891b2,color:#fff
    style B fill:#7c3aed,color:#fff
    style C fill:#db2777,color:#fff
    style D fill:#059669,color:#fff""",
    },
}


def generate_bar_chart(data, labels):
    max_val = max(data)
    bars = []
    for i, (val, label) in enumerate(zip(data, labels)):
        height = (val / max_val) * 100
        active = "active" if i == len(data) - 1 else ""
        bars.append(f"""<div class="bar-item">
        <div class="bar {active}" style="height: {height}%"><span class="bar-value">{val}</span></div>
        <span class="bar-label">{label}</span>
    </div>""")
    return "\n".join(bars)


def generate_pie_chart(pie_data):
    total = sum([c[1] for c in pie_data])
    cumulative = 0
    circles = []
    legend_items = []

    for label, pct, color in pie_data:
        dash = (pct / 100) * 188.5
        offset = -cumulative
        circles.append(
            f'''<circle cx="50" cy="50" r="30" fill="none" stroke="{color}" stroke-width="25" stroke-dasharray="{dash} 188.5" stroke-dashoffset="{offset}" transform="rotate(-90 50 50)"/>'''
        )
        legend_items.append(
            f"""<div class="legend-item"><span class="legend-color" style="background:{color}"></span>{label} {pct}%</div>"""
        )
        cumulative += dash

    return "\n".join(circles), "\n".join(legend_items), total


def generate_timeline(timeline_data):
    items = []
    for date, title, desc in timeline_data:
        items.append(f"""<div class="timeline-item">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
            <div class="timeline-date">{date}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
    </div>""")
    return "\n".join(items)


def generate_products_pie(products):
    colors = ["#0891b2", "#7c3aed", "#db2777", "#e2e8f0"]
    cumulative = 0
    circles = []
    legend_items = []

    for i, (label, pct) in enumerate(products):
        dash = (pct / 100) * 188.5
        offset = -cumulative
        circles.append(
            f'''<circle cx="50" cy="50" r="30" fill="none" stroke="{colors[i]}" stroke-width="25" stroke-dasharray="{dash} 188.5" stroke-dashoffset="{offset}" transform="rotate(-90 50 50)"/>'''
        )
        legend_items.append(
            f"""<div class="legend-item"><span class="legend-color" style="background:{colors[i]}"></span>{label} {pct}%</div>"""
        )
        cumulative += dash

    return "\n".join(circles), "\n".join(legend_items)


VISUALIZATION_TEMPLATE = """
            <section class="section">
                <h2 class="section-title"><span class="title-icon">▣</span>营收趋势</h2>
                <div class="charts-row">
                    <div class="chart-block fade-in" style="flex:2">
                        <div class="chart-header">
                            <h3>年度游戏营收趋势</h3>
                            <span class="chart-tag">单位: 亿元</span>
                        </div>
                        <div class="bar-chart">
                            {bar_chart}
                        </div>
                    </div>
                    <div class="chart-block fade-in fade-in-delay-1" style="flex:1">
                        <div class="chart-header">
                            <h3>收入构成</h3>
                            <span class="chart-tag">2026</span>
                        </div>
                        <div class="donut-chart-container">
                            <div class="donut-chart">
                                <svg viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="40" fill="none" stroke="#e2e8f0" stroke-width="12"/>
                                    {pie_chart_svg}
                                </svg>
                                <div class="donut-center">
                                    <span class="donut-value">{total_revenue}亿</span>
                                    <span class="donut-label">Total</span>
                                </div>
                            </div>
                            <div class="chart-legend">
                                {pie_legend}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="section">
                <h2 class="section-title"><span class="title-icon">▣</span>产品矩阵</h2>
                <div class="two-col-grid">
                    <div class="chart-block fade-in">
                        <div class="chart-header">
                            <h3>旗舰产品收入占比</h3>
                        </div>
                        <div class="pie-chart-container">
                            <div class="pie-chart">
                                <svg viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="30" fill="none" stroke="#e2e8f0" stroke-width="25"/>
                                    {products_svg}
                                </svg>
                            </div>
                            <div class="pie-legend">
                                {products_legend}
                            </div>
                        </div>
                    </div>
                    <div class="chart-block fade-in fade-in-delay-1">
                        <div class="chart-header">
                            <h3>产品发展历程</h3>
                        </div>
                        <div class="timeline" style="max-height:200px;overflow-y:auto">
                            {timeline}
                        </div>
                    </div>
                </div>
            </section>

            <section class="section">
                <h2 class="section-title"><span class="title-icon">▣</span>业务架构</h2>
                <div class="chart-block fade-in">
                    <pre class="mermaid">
{flowchart}
                    </pre>
                </div>
            </section>"""


def add_mermaid_script(content):
    if "mermaid.min.js" not in content:
        content = content.replace(
            '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">',
            """<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>""",
        )
    if "mermaid.initialize" not in content:
        content = content.replace(
            '<script src="navigation.js"></script>',
            """<script src="navigation.js"></script>
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'default', flowchart: { useMaxWidth: true } });
    </script>""",
        )
    return content


def update_file(filepath, data):
    if filepath not in data:
        return False

    company = data[filepath]
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already has visualizations
    if "营收趋势" in content:
        return False

    bar_chart = generate_bar_chart(company["revenue"], company["revenue_labels"])
    pie_svg, pie_legend, total = generate_pie_chart(company["pie_data"])
    products_svg, products_legend = generate_products_pie(company["products"])
    timeline = generate_timeline(company["timeline"])

    viz_html = VISUALIZATION_TEMPLATE.format(
        bar_chart=bar_chart,
        pie_chart_svg=pie_svg,
        pie_legend=pie_legend,
        products_svg=products_svg,
        products_legend=products_legend,
        timeline=timeline,
        flowchart=company["flowchart"],
        total_revenue=total,
    )

    content = content.replace("        </main>", viz_html + "\n        </main>")
    content = add_mermaid_script(content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    for filepath in COMPANY_DATA:
        if os.path.exists(filepath):
            if update_file(filepath, COMPANY_DATA):
                print(f"Updated: {filepath}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import re

# Company data for visualizations
COMPANY_DATA = {
    "tencent.html": {
        "title": "腾讯游戏",
        "revenue": [850, 1288, 1209, 1372, 1617, 1855, 2150],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [
            ("手游", 60, "#0891b2"),
            ("端游", 25, "#7c3aed"),
            ("其他", 15, "#db2777"),
        ],
        "products": [("王者荣耀", 30), ("和平精英", 25), ("DNF手游", 15), ("其他", 30)],
        "timeline": [
            ("2003", "QQ游戏大厅", "进入游戏市场"),
            ("2015", "王者荣耀上线", "移动电竞时代"),
            ("2019", "和平精英", "战术竞技手游"),
            ("2021", "DNF手游", "经典IP移动化"),
        ],
        "flowchart": """flowchart TB
    A[腾讯游戏] --> B[自研工作室]
    A --> C[投资收购]
    A --> D[代理发行]
    
    B --> B1[天美工作室]
    B --> B2[光子工作室]
    B --> B3[魔方工作室]
    B --> B4[北极光工作室]
    
    C --> C1[Riot Games]
    C --> C2[Epic Games]
    C --> C3[Supercell]
    
    D --> D1[国内发行]
    D --> D2[海外发行]
    
    B1 --> E[王者荣耀]
    B1 --> E2[和平精英]
    B2 --> E3[英雄联盟手游]
    B3 --> E4[DNF手游]
    
    style A fill:#0891b2,color:#fff
    style B fill:#7c3aed,color:#fff
    style C fill:#db2777,color:#fff
    style D fill:#059669,color:#fff""",
    },
    "netease.html": {
        "title": "网易游戏",
        "revenue": [500, 620, 580, 640, 720, 780, 820],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [
            ("手游", 55, "#0891b2"),
            ("端游", 35, "#7c3aed"),
            ("其他", 10, "#db2777"),
        ],
        "products": [("梦幻西游", 28), ("大话西游", 20), ("阴阳师", 15), ("其他", 37)],
        "timeline": [
            ("2001", "大话西游", "西游IP起源"),
            ("2003", "梦幻西游", "MMORPG经典"),
            ("2016", "阴阳师", "二次元突破"),
            ("2022", "蛋仔派对", "休闲竞技"),
        ],
        "flowchart": """flowchart TB
    A[网易游戏] --> B[自研产品]
    A --> C[IP运营]
    A --> D[海外发行]
    
    B --> B1[梦幻西游]
    B --> B2[大话西游]
    B --> B3[阴阳师]
    B --> B4[逆水寒]
    
    C --> C1[游戏改编]
    C --> C2[影视联动]
    C --> C3[文创衍生]
    
    D --> D1[日本市场]
    D --> D2[欧美市场]
    
    style A fill:#0891b2,color:#fff
    style B fill:#7c3aed,color:#fff
    style C fill:#db2777,color:#fff
    style D fill:#059669,color:#fff""",
    },
    "miyou.html": {
        "title": "米哈游",
        "revenue": [85, 180, 250, 380, 480, 540, 580],
        "revenue_labels": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
        "pie_data": [("海外", 62, "#0891b2"), ("国内", 38, "#7c3aed")],
        "products": [("原神", 45), ("崩坏星穹铁道", 30), ("崩坏3", 15), ("其他", 10)],
        "timeline": [
            ("2012", "崩坏学园", "创业起步"),
            ("2016", "崩坏3", "动作手游突破"),
            ("2020", "原神", "全球爆红"),
            ("2023", "崩坏星穹铁道", "回合制成功"),
        ],
        "flowchart": """flowchart TB
    A[米哈游] --> B[自研产品]
    A --> C[全球化]
    A --> D[IP生态]
    
    B --> B1[原神]
    B --> B2[崩坏星穹铁道]
    B --> B3[崩坏3]
    B --> B4[绝区零]
    
    C --> C1[海外发行]
    C --> C2[本地化]
    C --> C3[全球社区]
    
    D --> D1[动画]
    D --> D2[漫画]
    D --> D3[虚拟偶像]
    
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
    colors = [c[2] for c in pie_data]
    percentages = [c[1] for c in pie_data]
    labels = [c[0] for c in pie_data]

    total = sum(percentages)
    cumulative = 0
    circles = []
    legend_items = []

    for i, (label, pct, color) in enumerate(pie_data):
        dash = (pct / 100) * 188.5
        offset = -cumulative
        circles.append(
            f'''<circle cx="50" cy="50" r="30" fill="none" stroke="{color}" stroke-width="25" stroke-dasharray="{dash} 188.5" stroke-dashoffset="{offset}" transform="rotate(-90 50 50)"/>'''
        )
        legend_items.append(
            f"""<div class="legend-item"><span class="legend-color" style="background:{color}"></span>{label} {pct}%</div>"""
        )
        cumulative += dash

    return "\n".join(circles), "\n".join(legend_items)


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
    total = sum([p[1] for p in products])
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

    # Generate visualizations
    bar_chart = generate_bar_chart(company["revenue"], company["revenue_labels"])

    pie_svg, pie_legend = generate_pie_chart(company["pie_data"])
    products_svg, products_legend = generate_products_pie(company["products"])
    timeline = generate_timeline(company["timeline"])
    total_revenue = company["revenue"][-1]

    viz_html = VISUALIZATION_TEMPLATE.format(
        bar_chart=bar_chart,
        pie_chart_svg=pie_svg,
        pie_legend=pie_legend,
        products_svg=products_svg,
        products_legend=products_legend,
        timeline=timeline,
        flowchart=company["flowchart"],
        total_revenue=total_revenue,
    )

    # Insert before </main>
    content = content.replace("        </main>", viz_html + "\n        </main>")

    # Add mermaid script
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

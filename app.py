import streamlit as st
import plotly.graph_objects as go
from utils.data_generator import (
    generate_kpi_data, generate_hourly_flow, generate_city_flow,
    generate_scenic_top10, generate_scenic_type, generate_forecast,
    generate_alerts, generate_realtime_scenic
)
from datetime import datetime

st.set_page_config(
    page_title="云南文旅数据服务平台",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "云南文旅数据服务平台 v2.0"}
)

# ========== 全局样式 ==========
st.markdown("""
<style>
.stApp { background: #F7F9FC; }
header { visibility: hidden; }
.stDeployButton { display: none; }
footer { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 0.5rem !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none; }
.stButton > button {
    background: #fff !important; color: #4466E0 !important;
    border: 1px solid #4466E0 !important; border-radius: 6px !important;
    font-size: 12px !important; font-weight: 600 !important;
}
.stButton > button:hover { background: #4466E0 !important; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# ========== 模块1：顶部导航栏 ==========
header_html = f"""
<div style="display:flex; justify-content:space-between; align-items:center; background:#fff; border-radius:8px; padding:14px 24px; margin-bottom:16px; box-shadow:0 2px 12px rgba(68,102,224,0.08);">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:36px; height:36px; background:linear-gradient(135deg, #4466E0, #7D46D9); border-radius:8px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:18px;">云</div>
        <div>
            <div style="font-size:20px; font-weight:700; color:#1a1a2e;">云南文旅数据服务平台</div>
            <div style="font-size:11px; color:#888; letter-spacing:1px;">YUNNAN CULTURAL TOURISM DATA PLATFORM</div>
        </div>
    </div>
    <div style="text-align:center;">
        <div style="font-size:20px; font-weight:700; color:#1a1a2e; font-family:monospace;">{current_time}</div>
        <div style="font-size:11px; color:#888; margin-top:2px;">每 10 分钟自动同步全省景区客流</div>
    </div>
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="background:#F7F9FC; border:1px solid #e0e0e0; border-radius:6px; padding:5px 14px;"><span style="color:#555866; font-size:12px;">2026年度</span></div>
        <div style="background:#F7F9FC; border:1px solid #e0e0e0; border-radius:6px; padding:5px 14px;"><span style="color:#555866; font-size:12px;">全省</span></div>
        <div style="background:#4466E0; border-radius:6px; padding:6px 16px; cursor:pointer;"><span style="color:#fff; font-size:12px; font-weight:600;">导出报表</span></div>
    </div>
</div>
"""
st.html(header_html)

# ========== 模块2：核心KPI指标区 ==========
kpi_data = generate_kpi_data()
kpi_items = [
    ("全域覆盖景区", kpi_data["scenic"]["value"], kpi_data["scenic"]["unit"], kpi_data["scenic"]["sub"], kpi_data["scenic"]["change"], kpi_data["scenic"]["trend"], "#4466E0"),
    ("累计客流数据记录", kpi_data["records"]["value"], kpi_data["records"]["unit"], kpi_data["records"]["sub"], kpi_data["records"]["change"], kpi_data["records"]["trend"], "#7D46D9"),
    ("客流预测模型准确率", kpi_data["accuracy"]["value"], kpi_data["accuracy"]["unit"], kpi_data["accuracy"]["sub"], kpi_data["accuracy"]["change"], kpi_data["accuracy"]["trend"], "#34B868"),
    ("实时在园总游客", kpi_data["realtime"]["value"], kpi_data["realtime"]["unit"], kpi_data["realtime"]["sub"], kpi_data["realtime"]["change"], kpi_data["realtime"]["trend"], "#FF7D33"),
]

kpi_html = '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; margin-bottom:20px;">'
for title, value, unit, sub, change, trend, color in kpi_items:
    if trend == "up":
        arrow = "&#9650;"; change_color = "#34B868"; change_bg = "rgba(52,184,104,0.08)"
    elif trend == "down":
        arrow = "&#9660;"; change_color = "#E53E3E"; change_bg = "rgba(229,62,62,0.08)"
    else:
        arrow = "&#9472;"; change_color = "#888"; change_bg = "rgba(136,136,136,0.08)"
    change_text = f"{change:+.1f}%" if change != 0 else "持平"

    kpi_html += f"""
    <div style="background:#fff; border-radius:8px; padding:20px; box-shadow:0 2px 12px rgba(68,102,224,0.08); position:relative; overflow:hidden;">
        <div style="position:absolute; top:0; left:0; width:4px; height:100%; background:{color}; border-radius:8px 0 0 8px;"></div>
        <div style="font-size:13px; color:#555866; margin-bottom:10px; font-weight:500;">{title}</div>
        <div style="display:flex; align-items:baseline; gap:4px; margin-bottom:8px;">
            <span style="font-size:32px; font-weight:800; color:#1a1a2e;">{value}</span>
            <span style="font-size:14px; color:#888;">{unit}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#888; font-size:12px;">{sub}</span>
            <span style="background:{change_bg}; color:{change_color}; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">{arrow} {change_text}</span>
        </div>
        <div style="margin-top:12px; height:3px; background:#f0f0f0; border-radius:2px; overflow:hidden;">
            <div style="width:70%; height:100%; background:{color}; border-radius:2px;"></div>
        </div>
    </div>"""
kpi_html += '</div>'
st.html(kpi_html)

# ========== 模块3：全域客流总览可视化 ==========
st.html("""
<div style="display:flex; align-items:center; gap:10px; margin:24px 0 16px 0;">
    <div style="width:4px; height:20px; background:linear-gradient(180deg, #4466E0, #7D46D9); border-radius:2px;"></div>
    <span style="font-size:18px; font-weight:700; color:#1a1a2e;">全域客流总览</span>
    <div style="flex:1; height:1px; background:#e0e0e0;"></div>
</div>
""")

col_map, col_trend = st.columns([2, 3])

with col_map:
    st.markdown("<p style='color:#555866; font-size:13px; font-weight:600; margin-bottom:8px;'>云南省州市客流分布</p>", unsafe_allow_html=True)
    city_df = generate_city_flow()
    fig_map = go.Figure()
    fig_map.add_trace(go.Bar(
        y=city_df["州市"], x=city_df["客流(万)"], orientation="h",
        marker=dict(color=["#4466E0" if i < 3 else "#7D46D9" if i < 6 else "#94a3b8" for i in range(len(city_df))], line=dict(color="#fff", width=1)),
        text=[f"{v}万" for v in city_df["客流(万)"]], textposition="outside", textfont=dict(color="#555866", size=11),
        hovertemplate="<b>%{y}</b><br>客流: %{x}万<extra></extra>",
    ))
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=50, t=10, b=10), height=320,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#1a1a2e", size=12)),
        bargap=0.4,
    )
    st.plotly_chart(fig_map, use_container_width=True, key="city_map")

with col_trend:
    st.markdown("<p style='color:#555866; font-size:13px; font-weight:600; margin-bottom:8px;'>24小时分时客流趋势</p>", unsafe_allow_html=True)
    flow_df = generate_hourly_flow()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=flow_df["时间"], y=flow_df["今日"], mode="lines",
        line=dict(color="#4466E0", width=2.5), fill="tozeroy", fillcolor="rgba(68,102,224,0.1)",
        name="今日实时", hovertemplate="<b>%{x}</b><br>今日: %{y}万<extra></extra>",
    ))
    fig_trend.add_trace(go.Scatter(
        x=flow_df["时间"], y=flow_df["去年同期"], mode="lines",
        line=dict(color="#FF7D33", width=2, dash="dash"),
        name="去年同期", hovertemplate="<b>%{x}</b><br>去年: %{y}万<extra></extra>",
    ))
    fig_trend.add_hline(y=12, line_dash="dot", line_color="#E53E3E", annotation_text="承载上限", annotation_position="right")
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=80, t=10, b=40), height=320,
        xaxis=dict(showgrid=False, tickfont=dict(color="#555866", size=10), nticks=8),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", tickfont=dict(color="#555866", size=11), title="客流(万)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
    )
    st.plotly_chart(fig_trend, use_container_width=True, key="flow_trend")

# ========== 模块4：平台三大能力多维分析 ==========
st.html("""
<div style="display:flex; align-items:center; gap:10px; margin:24px 0 16px 0;">
    <div style="width:4px; height:20px; background:linear-gradient(180deg, #4466E0, #7D46D9); border-radius:2px;"></div>
    <span style="font-size:18px; font-weight:700; color:#1a1a2e;">平台核心能力</span>
    <div style="flex:1; height:1px; background:#e0e0e0;"></div>
</div>
""")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("<p style='color:#4466E0; font-size:15px; font-weight:700; margin-bottom:8px;'>景点总览</p>", unsafe_allow_html=True)
    top_df = generate_scenic_top10().head(5)
    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(
        y=list(reversed(top_df["景区"].tolist())), x=list(reversed(top_df["客流(万)"].tolist())), orientation="h",
        marker=dict(color="#4466E0", line=dict(color="#fff", width=1)),
        text=[f"{v}万" for v in reversed(top_df["客流(万)"].tolist())], textposition="outside", textfont=dict(color="#555866", size=10),
        hovertemplate="<b>%{y}</b><br>客流: %{x}万<extra></extra>",
    ))
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=100, r=40, t=5, b=5), height=200,
        xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False, tickfont=dict(color="#1a1a2e", size=11)),
        bargap=0.5,
    )
    st.plotly_chart(fig_top, use_container_width=True, key="cap_top")
    st.markdown("<p style='color:#888; font-size:12px; margin-top:6px;'>全省景点信息检索、多维度筛选、景区基础画像查看</p>", unsafe_allow_html=True)

with col_b:
    st.markdown("<p style='color:#7D46D9; font-size:15px; font-weight:700; margin-bottom:8px;'>流量分析</p>", unsafe_allow_html=True)
    type_df = generate_scenic_type()
    fig_type = go.Figure(data=[go.Pie(
        labels=type_df["类型"], values=type_df["客流(万)"], hole=0.6,
        textinfo="label+percent", textfont=dict(size=10, color="#1a1a2e"),
        marker=dict(colors=["#4466E0", "#7D46D9", "#34B868", "#FF7D33", "#E53E3E"], line=dict(color="#fff", width=2)),
        hovertemplate="<b>%{label}</b><br>客流: %{value}万<extra></extra>",
    )])
    fig_type.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=5, b=5), height=200, showlegend=False,
        annotations=[dict(text="类型", x=0.5, y=0.5, font_size=14, font_color="#555866", showarrow=False)],
    )
    st.plotly_chart(fig_type, use_container_width=True, key="cap_type")
    st.markdown("<p style='color:#888; font-size:12px; margin-top:6px;'>分时 / 月度客流统计、流量波动归因分析、拥堵识别</p>", unsafe_allow_html=True)

with col_c:
    st.markdown("<p style='color:#34B868; font-size:15px; font-weight:700; margin-bottom:8px;'>智能预测</p>", unsafe_allow_html=True)
    forecast_df = generate_forecast()
    fig_fore = go.Figure()
    fig_fore.add_trace(go.Scatter(
        x=forecast_df["日期"], y=forecast_df["预测"], mode="lines+markers",
        line=dict(color="#34B868", width=2), marker=dict(size=5),
        name="预测", hovertemplate="<b>%{x}</b><br>预测: %{y}万<extra></extra>",
    ))
    fig_fore.add_trace(go.Scatter(
        x=forecast_df["日期"], y=forecast_df["上限"], mode="lines",
        line=dict(color="#34B868", width=0), showlegend=False, hoverinfo="skip",
    ))
    fig_fore.add_trace(go.Scatter(
        x=forecast_df["日期"], y=forecast_df["下限"], mode="lines",
        line=dict(color="#34B868", width=0), fill="tonexty", fillcolor="rgba(52,184,104,0.1)",
        name="置信区间", hoverinfo="skip",
    ))
    fig_fore.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=5, b=30), height=200,
        xaxis=dict(showgrid=False, tickfont=dict(color="#555866", size=10)),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", tickfont=dict(color="#555866", size=10)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9)),
    )
    st.plotly_chart(fig_fore, use_container_width=True, key="cap_fore")
    st.markdown("<p style='color:#888; font-size:12px; margin-top:6px;'>机器学习时序预测、客流超载预警、错峰游览建议</p>", unsafe_allow_html=True)

# ========== 模块5：底部实时监控预警区 ==========
st.html("""
<div style="display:flex; align-items:center; gap:10px; margin:24px 0 16px 0;">
    <div style="width:4px; height:20px; background:linear-gradient(180deg, #E53E3E, #FF7D33); border-radius:2px;"></div>
    <span style="font-size:18px; font-weight:700; color:#1a1a2e;">实时监控预警</span>
    <div style="flex:1; height:1px; background:#e0e0e0;"></div>
</div>
""")

col_alert, col_table = st.columns([1, 1])

with col_alert:
    st.markdown("<p style='color:#555866; font-size:13px; font-weight:600; margin-bottom:10px;'>客流风险告警看板</p>", unsafe_allow_html=True)

    # 统计卡片
    alert_stats_html = """
    <div style="display:flex; gap:10px; margin-bottom:14px;">
        <div style="flex:1; background:#fff; border:1px solid #E53E3E; border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:22px; font-weight:800; color:#E53E3E;">1</div>
            <div style="font-size:11px; color:#E53E3E; margin-top:2px;">高危拥堵</div>
        </div>
        <div style="flex:1; background:#fff; border:1px solid #FF7D33; border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:22px; font-weight:800; color:#FF7D33;">2</div>
            <div style="font-size:11px; color:#FF7D33; margin-top:2px;">中危预警</div>
        </div>
        <div style="flex:1; background:#fff; border:1px solid #34B868; border-radius:8px; padding:12px; text-align:center;">
            <div style="font-size:22px; font-weight:800; color:#34B868;">5</div>
            <div style="font-size:11px; color:#34B868; margin-top:2px;">正常运营</div>
        </div>
    </div>
    """
    st.html(alert_stats_html)

    alert_df = generate_alerts()
    for _, row in alert_df.iterrows():
        level_color = {"高危": "#E53E3E", "中危": "#FF7D33", "正常": "#34B868"}[row["等级"]]
        level_bg = {"高危": "#FEF2F2", "中危": "#FFF7ED", "正常": "#F0FDF4"}[row["等级"]]

        alert_html = f"""
        <div style="background:#fff; border-radius:6px; padding:12px 14px; margin-bottom:8px; border-left:3px solid {level_color}; box-shadow:0 1px 4px rgba(0,0,0,0.04);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="background:{level_bg}; color:{level_color}; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">{row["等级"]}</span>
                    <span style="color:#1a1a2e; font-weight:600; font-size:13px;">{row["景区"]}</span>
                </div>
                <span style="color:#888; font-size:11px;">{row["当前客流"]}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#555866; font-size:12px;">承载率 {row["承载率"]} | {row["建议"]}</span>
            </div>
        </div>
        """
        st.html(alert_html)

with col_table:
    st.markdown("<p style='color:#555866; font-size:13px; font-weight:600; margin-bottom:10px;'>实时景区客流流水</p>", unsafe_allow_html=True)
    scenic_df = generate_realtime_scenic()

    table_html = """
    <table style="width:100%; border-collapse:collapse; font-size:12px; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <thead>
            <tr style="background:#F7F9FC;">
                <th style="padding:10px 12px; text-align:left; color:#555866; font-weight:600; border-bottom:1px solid #e0e0e0; font-size:12px;">景区</th>
                <th style="padding:10px 12px; text-align:right; color:#555866; font-weight:600; border-bottom:1px solid #e0e0e0; font-size:12px;">实时人数</th>
                <th style="padding:10px 12px; text-align:center; color:#555866; font-weight:600; border-bottom:1px solid #e0e0e0; font-size:12px;">拥堵等级</th>
            </tr>
        </thead>
        <tbody>
    """
    level_colors = {"高危": ("#FEF2F2", "#E53E3E"), "中危": ("#FFF7ED", "#FF7D33"), "正常": ("#F0FDF4", "#34B868")}
    for _, row in scenic_df.iterrows():
        bg, color = level_colors.get(row["拥堵等级"], ("#F7F9FC", "#888"))
        table_html += f"""
        <tr style="border-bottom:1px solid #f0f0f0;">
            <td style="padding:10px 12px; color:#1a1a2e; font-weight:500;">{row["景区"]}</td>
            <td style="padding:10px 12px; color:#1a1a2e; text-align:right; font-family:monospace;">{row["实时人数"]:,}</td>
            <td style="padding:10px 12px; text-align:center;">
                <span style="background:{bg}; color:{color}; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">{row["拥堵等级"]}</span>
            </td>
        </tr>
        """
    table_html += "</tbody></table>"
    st.html(table_html)

# ========== 页脚 ==========
st.html("""
<div style="text-align:center; padding:20px; margin-top:20px; color:#888; font-size:12px;">
    云南文旅数据服务平台 | 数据每 10 分钟自动同步 | 技术支持：云南省文化和旅游厅
</div>
""")

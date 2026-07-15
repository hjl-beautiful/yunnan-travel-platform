import streamlit as st
import pandas as pd
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

st.set_page_config(page_title="数据分析", page_icon="", layout="wide")

st.markdown("<h2>数据分析</h2>", unsafe_allow_html=True)

SPOTS_DATA = {
    "name": [
        "丽江古城", "大理洱海", "玉龙雪山", "西双版纳热带植物园", "石林风景区",
        "泸沽湖", "香格里拉普达措", "腾冲火山热海", "元阳梯田", "梅里雪山",
        "虎跳峡", "束河古镇", "崇圣寺三塔", "苍山", "滇池",
        "九乡溶洞", "建水古城", "普者黑", "坝美", "丙中洛"
    ],
    "city": [
        "丽江", "大理", "丽江", "西双版纳", "昆明",
        "丽江", "迪庆", "保山", "红河", "迪庆",
        "丽江", "丽江", "大理", "大理", "昆明",
        "昆明", "红河", "文山", "文山", "怒江"
    ],
    "type": [
        "古镇", "湖泊", "雪山", "植物园", "地质奇观",
        "湖泊", "国家公园", "温泉", "梯田", "雪山",
        "峡谷", "古镇", "古建筑", "山脉", "湖泊",
        "溶洞", "古城", "喀斯特", "村落", "峡谷"
    ],
    "rating": [4.8, 4.7, 4.9, 4.6, 4.5, 4.7, 4.8, 4.4, 4.6, 4.9,
               4.5, 4.6, 4.7, 4.5, 4.3, 4.4, 4.6, 4.5, 4.3, 4.7],
    "ticket_price": [50, 0, 130, 80, 130, 70, 100, 40, 70, 0,
                     65, 0, 75, 0, 0, 90, 0, 85, 0, 0],
    "annual_visitors": [1500, 1200, 800, 600, 400, 350, 300, 200, 180, 150,
                        280, 320, 450, 380, 500, 220, 260, 190, 120, 80],
}

df = pd.DataFrame(SPOTS_DATA)

st.markdown("### 城市景点分布")
city_counts = df.groupby("city").size().reset_index(name="count")
city_counts = city_counts.sort_values("count", ascending=True)

bar = (
    Bar()
    .add_xaxis(city_counts["city"].tolist())
    .add_yaxis("景点数量", city_counts["count"].tolist(), itemstyle_opts=opts.ItemStyleOpts(color="#667eea"))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各城市景点数量"),
        xaxis_opts=opts.AxisOpts(name="城市"),
        yaxis_opts=opts.AxisOpts(name="数量"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    .reversal_axis()
)
st_pyecharts(bar, height="400px")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 景点类型分布")
    type_counts = df.groupby("type").size().reset_index(name="count")
    pie = (
        Pie()
        .add("", [list(z) for z in zip(type_counts["type"].tolist(), type_counts["count"].tolist())])
        .set_global_opts(title_opts=opts.TitleOpts(title="类型占比"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    st_pyecharts(pie, height="350px")

with col2:
    st.markdown("### 评分分布")
    rating_bins = pd.cut(df["rating"], bins=[0, 4.0, 4.3, 4.6, 4.8, 5.0], labels=["<4.0", "4.0-4.3", "4.3-4.6", "4.6-4.8", ">4.8"])
    rating_counts = rating_bins.value_counts().sort_index()
    bar2 = (
        Bar()
        .add_xaxis(rating_counts.index.tolist())
        .add_yaxis("景点数量", rating_counts.values.tolist(), itemstyle_opts=opts.ItemStyleOpts(color="#764ba2"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分区间分布"),
            xaxis_opts=opts.AxisOpts(name="评分区间"),
            yaxis_opts=opts.AxisOpts(name="数量"),
        )
    )
    st_pyecharts(bar2, height="350px")

st.markdown("---")
st.markdown("### 游客量趋势（模拟月度数据）")

months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
visitor_trend = [45, 52, 68, 85, 95, 78, 120, 135, 90, 110, 75, 55]

line = (
    Line()
    .add_xaxis(months)
    .add_yaxis(
        "游客量(万)",
        visitor_trend,
        is_smooth=True,
        symbol="circle",
        symbol_size=8,
        linestyle_opts=opts.LineStyleOpts(width=3, color="#667eea"),
        itemstyle_opts=opts.ItemStyleOpts(color="#667eea"),
        area_style_opts=opts.AreaStyleOpts(opacity=0.3, color="#667eea"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2024年云南旅游月度游客量趋势"),
        xaxis_opts=opts.AxisOpts(name="月份"),
        yaxis_opts=opts.AxisOpts(name="游客量(万人次)"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
    )
)
st_pyecharts(line, height="400px")

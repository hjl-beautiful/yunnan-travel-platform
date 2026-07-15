import streamlit as st
import pandas as pd
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_spots_data

st.set_page_config(page_title="数据分析", page_icon="", layout="wide")

st.markdown("<h2>数据分析</h2>", unsafe_allow_html=True)

df = load_spots_data()

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

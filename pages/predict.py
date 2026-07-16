import streamlit as st
import plotly.graph_objects as go
from utils.data_generator import generate_forecast

st.set_page_config(page_title="智能预测", page_icon="", layout="wide")

st.markdown("<h2 style='color:#1a1a2e; margin-bottom:20px;'>智能预测</h2>", unsafe_allow_html=True)

df = generate_forecast()

st.markdown("<p style='color:#555866; font-size:14px; margin-bottom:12px;'>未来 7 天客流预测曲线，标注高拥堵预警区间</p>", unsafe_allow_html=True)

fig = go.Figure()

# 置信区间
fig.add_trace(go.Scatter(
    x=df["日期"].tolist() + df["日期"].tolist()[::-1],
    y=df["上限"].tolist() + df["下限"].tolist()[::-1],
    fill="toself", fillcolor="rgba(68,102,224,0.1)",
    line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip",
    name="预测区间",
))

# 预测线
fig.add_trace(go.Scatter(
    x=df["日期"], y=df["预测"], mode="lines+markers",
    line=dict(color="#4466E0", width=2.5),
    marker=dict(size=6, color="#4466E0"),
    name="预测客流",
    hovertemplate="<b>%{x}</b><br>预测客流: %{y}万<extra></extra>",
))

# 预警线
fig.add_hline(y=30, line_dash="dash", line_color="#E53E3E", annotation_text="拥堵预警线", annotation_position="right")

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=50, r=80, t=20, b=40), height=350,
    xaxis=dict(showgrid=False, tickfont=dict(color="#555866", size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", tickfont=dict(color="#555866", size=11), title="客流(万)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True, key="forecast_chart")

st.markdown("<p style='color:#555866; font-size:13px; margin-top:10px;'>机器学习时序预测、客流超载预警、错峰游览建议</p>", unsafe_allow_html=True)

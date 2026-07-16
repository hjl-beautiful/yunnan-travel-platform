import streamlit as st
import plotly.graph_objects as go
from utils.data_generator import generate_scenic_top10

st.set_page_config(page_title="景点总览", page_icon="", layout="wide")

st.markdown("<h2 style='color:#1a1a2e; margin-bottom:20px;'>景点总览</h2>", unsafe_allow_html=True)

df = generate_scenic_top10()

st.markdown("<p style='color:#555866; font-size:14px; margin-bottom:12px;'>全省 TOP10 热门景区累计接待游客排行</p>", unsafe_allow_html=True)

fig = go.Figure()
colors = ["#4466E0" if row["等级"] == "5A" else "#7D46D9" for _, row in df.iterrows()]
fig.add_trace(go.Bar(
    y=list(reversed(df["景区"].tolist())),
    x=list(reversed(df["客流(万)"].tolist())),
    orientation="h",
    marker=dict(color=list(reversed(colors)), line=dict(color="#fff", width=1)),
    text=[f"{v}万" for v in reversed(df["客流(万)"].tolist())],
    textposition="outside",
    textfont=dict(color="#555866", size=12),
    hovertemplate="<b>%{y}</b><br>客流: %{x}万<extra></extra>",
))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=120, r=50, t=20, b=20), height=400,
    xaxis=dict(showgrid=False, showticklabels=False),
    yaxis=dict(showgrid=False, tickfont=dict(color="#1a1a2e", size=13)),
    bargap=0.35,
)
st.plotly_chart(fig, use_container_width=True, key="scenic_top10")

st.markdown("<p style='color:#555866; font-size:13px; margin-top:10px;'>全省景点信息检索、多维度筛选、景区基础画像查看</p>", unsafe_allow_html=True)

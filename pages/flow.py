import streamlit as st
import plotly.graph_objects as go
from utils.data_generator import generate_scenic_type

st.set_page_config(page_title="流量分析", page_icon="", layout="wide")

st.markdown("<h2 style='color:#1a1a2e; margin-bottom:20px;'>流量分析</h2>", unsafe_allow_html=True)

df = generate_scenic_type()

st.markdown("<p style='color:#555866; font-size:14px; margin-bottom:12px;'>景区类型客流占比分布</p>", unsafe_allow_html=True)

fig = go.Figure(data=[go.Pie(
    labels=df["类型"], values=df["客流(万)"], hole=0.55,
    textinfo="label+percent", textfont=dict(size=12, color="#1a1a2e"),
    marker=dict(colors=["#4466E0", "#7D46D9", "#34B868", "#FF7D33", "#E53E3E"], line=dict(color="#fff", width=2)),
    hovertemplate="<b>%{label}</b><br>客流: %{value}万<br>占比: %{percent}<extra></extra>",
)])
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=20, b=0), height=350, showlegend=False,
    annotations=[dict(text="景区类型", x=0.5, y=0.5, font_size=16, font_color="#555866", showarrow=False)],
)
st.plotly_chart(fig, use_container_width=True, key="flow_type")

st.markdown("<p style='color:#555866; font-size:13px; margin-top:10px;'>分时 / 月度客流统计、流量波动归因分析、拥堵识别</p>", unsafe_allow_html=True)

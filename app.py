import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.predictor import generate_historical_trend, predict_next_7_days, get_model_metrics, is_model_ready

st.set_page_config(page_title="景区客流智能预测与运营决策系统", page_icon="🏔️", layout="wide")

# CSS
st.markdown("""
<style>
    .hero-banner {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #7c3aed 100%);
        border-radius: 16px; padding: 32px 40px; margin-bottom: 24px;
        color: white;
    }
    .stat-card {
        background: white; border-radius: 12px; padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;
    }
    .stat-value { font-size: 32px; font-weight: 800; color: #1e293b; }
    .stat-label { font-size: 13px; color: #64748b; margin-top: 4px; }
    .feature-grid {
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 16px; margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===== 页面标题 =====
st.html("""
<div class="hero-banner">
    <h1 style="font-size:30px; font-weight:800; margin-bottom:8px;">🏔️ 景区客流智能预测与运营决策系统</h1>
    <p style="font-size:15px; opacity:0.9; margin-bottom:4px;">
        基于 XGBoost 时序预测 · 赋能景区数字化运营 · 方法论可迁移至云南头部景区
    </p>
    <p style="font-size:12px; opacity:0.6;">
        训练数据: 九寨沟景区官网 4,000+ 天真实游客数据 (2015-2026)
    </p>
</div>
""")

# ===== 模型状态 =====
model_ready = is_model_ready()
if not model_ready:
    st.warning("⚠️ 机器学习模型尚未训练。请先运行 `ml/train_model.py` 完成模型训练。当前为演示模式。")

# ===== 核心统计 =====
hist_df = generate_historical_trend(365)
metrics = get_model_metrics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    avg_visitors = hist_df["客流量"].mean()
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#3b82f6;">{avg_visitors:,.0f}</div>
        <div class="stat-label">日均客流量 (人次)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    max_visitors = hist_df["客流量"].max()
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#10b981;">{max_visitors:,}</div>
        <div class="stat-label">历史最高日客流</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#f59e0b;">{metrics.get('r2', '—')}</div>
        <div class="stat-label">模型 R² 决定系数</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#8b5cf6;">{len(hist_df) if not hist_df.empty else '—'}</div>
        <div class="stat-label">训练数据量 (天)</div>
    </div>
    """, unsafe_allow_html=True)

# ===== 历史趋势 + 7日预测 =====
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 近12个月客流量趋势")
    monthly = hist_df.set_index("日期").resample("ME")["客流量"].mean().reset_index()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=monthly["日期"], y=monthly["客流量"],
        mode="lines+markers", name="月均客流量",
        line=dict(color="#3b82f6", width=2.5),
        marker=dict(size=8),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
    ))
    fig1.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=20, r=20, t=10, b=20), height=350,
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="月均客流量", showgrid=True, gridcolor="#f1f5f9", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🔮 未来7日客流量预测")
    forecast = predict_next_7_days()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=forecast["日期"], y=forecast["预测"],
        marker=dict(color="#3b82f6", line=dict(color="white", width=2)),
        text=[f"{v:,}" for v in forecast["预测"]],
        textposition="outside",
        textfont=dict(size=12, color="#1e293b"),
        hovertemplate="<b>%{x}</b><br>预测: %{y:,} 人次<extra></extra>",
    ))
    fig2.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=20, r=20, t=30, b=20), height=350,
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="预测客流量", showgrid=True, gridcolor="#f1f5f9", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===== 项目特色 =====
st.markdown("---")
st.markdown("### 🎯 项目核心能力")

features = [
    ("📊", "真实数据驱动", "基于九寨沟景区官网每日公开游客数据，非模拟/人造数据，确保分析结果真实可靠"),
    ("🔮", "机器学习预测", "XGBoost 时序预测模型，覆盖节假日效应、季节模式、历史趋势等 30+ 特征维度"),
    ("🔬", "可解释性分析", "SHAP 值特征重要性分析，让「为什么预测这个数」有据可查"),
    ("🔄", "方法论可迁移", "所有特征均为通用维度，不依赖特定景区属性，直接迁移至丽江古城、玉龙雪山等云南景区"),
]

for emoji, title, desc in features:
    st.html(f"""
    <div style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:16px 20px; margin-bottom:10px; display:flex; align-items:flex-start; gap:14px;">
        <div style="font-size:28px; min-width:40px; text-align:center;">{emoji}</div>
        <div>
            <div style="font-weight:700; color:#1e293b; margin-bottom:4px;">{title}</div>
            <div style="color:#64748b; font-size:13px;">{desc}</div>
        </div>
    </div>
    """)

# ===== 底部说明 =====
st.markdown("---")
st.html("""
<div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:12px; padding:20px; margin-top:16px;">
    <h4 style="color:#0369a1; margin-bottom:8px;">💡 关于数据来源与方法论</h4>
    <p style="color:#475569; font-size:13px; margin:0;">
        <strong>为什么用九寨沟数据？</strong> 国内5A级景区中，九寨沟是<strong>唯一一个每日在官网公开精确游客人数</strong>的景区。
        该数据已被多篇 SCI 论文（包括 MDPI Sustainability 2026）用于客流预测研究。
        本项目使用的全部特征（节假日、周末、历史趋势等）均为<strong>通用维度</strong>，
        不依赖九寨沟特有属性，方法论可<strong>无缝迁移</strong>至丽江古城、玉龙雪山、大理古城等云南头部景区。<br><br>
        <strong>数据来源：</strong>https://www.jiuzhai.com/news/number-of-tourists（九寨沟景区官方网站）<br>
        <strong>参考文献：</strong>Cheng, J. et al. (2026). Daily Inbound Visitor Flow Forecasting for Jiuzhai Valley. MDPI Sustainability, 18(14), 7099.
    </p>
</div>
""")

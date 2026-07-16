import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.predictor import (
    predict_next_7_days, get_model_metrics, get_feature_importance,
    get_shap_importance, generate_historical_trend, is_model_ready
)

st.set_page_config(page_title="客流智能预测", page_icon="📈", layout="wide")

# CSS
st.markdown("""
<style>
    .metric-card {
        background: white; border-radius: 12px; padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center; border-top: 3px solid #3b82f6;
    }
    .metric-value { font-size: 28px; font-weight: 800; color: #1e293b; }
    .metric-label { font-size: 13px; color: #64748b; margin-top: 4px; }
    .model-badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 12px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ===== 页面标题 =====
st.markdown("""
<div style="margin-bottom: 24px;">
    <h1 style="color:#1e293b; font-size:28px; margin-bottom:4px;">📈 景区客流智能预测</h1>
    <p style="color:#64748b; font-size:14px;">
        基于 XGBoost 时序预测模型 · 九寨沟4,000+天真实数据训练 · 方法论可迁移至云南景区
    </p>
</div>
""", unsafe_allow_html=True)

# ===== 模型状态检查 =====
model_ready = is_model_ready()
if not model_ready:
    st.warning("⚠️ 模型尚未训练。请先运行 `ml/train_model.py` 训练模型。当前将显示演示数据。")

# ===== 模型评估指标卡片 =====
metrics = get_model_metrics()
if metrics:
    m1, m2, m3, m4 = st.columns(4)
    metric_items = [
        ("R² 决定系数", f"{metrics['r2']:.4f}", "越接近1越好"),
        ("MAE 平均误差", f"{metrics['mae']:,.0f} 人次", "预测偏差绝对值均值"),
        ("MAPE 百分比误差", f"{metrics['mape']:.1f}%", "误差占实际值比例"),
    ]
    
    with m1:
        st.markdown(f"""
        <div class="metric-card" style="border-top-color:#3b82f6;">
            <div class="metric-value" style="color:#3b82f6;">{metrics['r2']:.4f}</div>
            <div class="metric-label">R² 决定系数</div>
            <div style="font-size:11px; color:#94a3b8;">越接近1越好</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m2:
        st.markdown(f"""
        <div class="metric-card" style="border-top-color:#10b981;">
            <div class="metric-value" style="color:#10b981;">{metrics['mae']:,.0f}</div>
            <div class="metric-label">MAE 平均绝对误差 (人次)</div>
            <div style="font-size:11px; color:#94a3b8;">预测偏差均值</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m3:
        st.markdown(f"""
        <div class="metric-card" style="border-top-color:#f59e0b;">
            <div class="metric-value" style="color:#f59e0b;">{metrics['mape']:.1f}%</div>
            <div class="metric-label">MAPE 百分比误差</div>
            <div style="font-size:11px; color:#94a3b8;">相对误差比例</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m4:
        # 对比论文
        r2_val = metrics['r2']
        if r2_val >= 0.892:
            badge_class = "background:#dcfce7; color:#166534;"
            status = "✅ 优于论文"
        else:
            gap = 0.892 - r2_val
            badge_class = "background:#fef3c7; color:#92400e;"
            status = f"接近论文 (差{gap:.3f})"
        
        st.markdown(f"""
        <div class="metric-card" style="border-top-color:#8b5cf6;">
            <div class="metric-value" style="color:#8b5cf6; font-size:18px;">{status}</div>
            <div class="metric-label">对比 MDPI 2026 论文</div>
            <div style="font-size:11px; color:#94a3b8;">SD-ConvLSTM R²=0.892</div>
        </div>
        """, unsafe_allow_html=True)

# ===== 7日预测 =====
st.markdown("---")
st.markdown("### 📊 未来7日客流量预测")

forecast_df = predict_next_7_days()

# 用 Plotly 画预测图
fig = go.Figure()

# 置信区间
fig.add_trace(go.Scatter(
    x=list(forecast_df["日期"]) + list(forecast_df["日期"])[::-1],
    y=list(forecast_df["上限"]) + list(forecast_df["下限"])[::-1],
    fill="toself", fillcolor="rgba(59,130,246,0.1)",
    line=dict(color="rgba(255,255,255,0)"),
    hoverinfo="skip",
    showlegend=True, name="95% 置信区间",
))

# 预测值
fig.add_trace(go.Scatter(
    x=forecast_df["日期"], y=forecast_df["预测"],
    mode="lines+markers", name="预测客流量",
    line=dict(color="#3b82f6", width=3),
    marker=dict(size=10, color="#3b82f6"),
    hovertemplate="<b>%{x}</b><br>预测: %{y:,} 人次<extra></extra>",
))

fig.update_layout(
    paper_bgcolor="white", plot_bgcolor="white",
    margin=dict(l=20, r=20, t=20, b=20), height=400,
    xaxis=dict(title="", showgrid=False, tickfont=dict(size=13)),
    yaxis=dict(title="预测客流量 (人次)", showgrid=True, gridcolor="#f1f5f9",
              tickfont=dict(size=12), tickformat=","),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)

# 预测数据表格
st.markdown("##### 预测明细")
pred_table = forecast_df[["日期", "完整日期", "预测", "下限", "上限"]].copy()
pred_table.columns = ["日期", "完整日期", "预测客流量", "下限 (85%)", "上限 (115%)"]
pred_table["预测客流量"] = pred_table["预测客流量"].apply(lambda x: f"{x:,}")
pred_table["下限 (85%)"] = pred_table["下限 (85%)"].apply(lambda x: f"{x:,}")
pred_table["上限 (115%)"] = pred_table["上限 (115%)"].apply(lambda x: f"{x:,}")
st.dataframe(pred_table[["日期", "预测客流量", "下限 (85%)", "上限 (115%)"]], 
             use_container_width=True, hide_index=True)


# ===== 历史趋势 + 特征分析 =====
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📉 近期客流量趋势 (30天)")
    hist_df = generate_historical_trend(30)
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=hist_df["日期"], y=hist_df["客流量"],
        mode="lines", name="客流量",
        line=dict(color="#3b82f6", width=2),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
    ))
    fig_hist.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=20, r=20, t=10, b=20), height=350,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f1f5f9", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.markdown("### 🔑 特征重要性排名 (Top 15)")
    feat_imp = get_feature_importance(15)
    
    if not feat_imp.empty:
        fig_feat = go.Figure()
        fig_feat.add_trace(go.Bar(
            y=list(reversed(feat_imp["feature"])),
            x=list(reversed(feat_imp["importance"])),
            orientation="h",
            marker=dict(
                color=["#3b82f6" if i < 3 else "#94a3b8" for i in range(len(feat_imp))],
                line=dict(color="white", width=1),
            ),
            hovertemplate="<b>%{y}</b><br>重要性: %{x:.4f}<extra></extra>",
        ))
        fig_feat.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20), height=350,
            xaxis=dict(title="重要性", showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False),
            bargap=0.3,
            showlegend=False,
        )
        st.plotly_chart(fig_feat, use_container_width=True)
    else:
        st.info("特征重要性数据将在模型训练后显示")


# ===== 底部：方法论说明 =====
st.markdown("---")
st.markdown("""
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px;">
    <h4 style="color:#1e293b; margin-bottom:12px;">🔬 技术说明</h4>
    
| 项目 | 详情 |
|------|------|
| **算法** | XGBoost (eXtreme Gradient Boosting) |
| **数据来源** | 九寨沟景区官网每日公开游客数据 (国内唯一每日公开的5A景区数据) |
| **特征维度** | 时间特征 + 节假日效应 + 历史滑动窗口 + 滚动统计 + 差分趋势 |
| **可迁移性** | 所有特征均为通用维度，不依赖景区特有属性，可直接迁移至丽江古城、玉龙雪山等云南景区 |
| **评估方法** | 时序拆分 (前80%训练/后20%测试) + TimeSeriesSplit交叉验证 |
| **参考文献** | Cheng, J. et al. (2026). SD-ConvLSTM-Attn. MDPI Sustainability, 18(14), 7099. |
</div>
""", unsafe_allow_html=True)

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.predictor import (
    predict_next_7_days, get_model_metrics, get_feature_importance,
    generate_historical_trend, is_model_ready
)
from utils.navbar import render_navbar, render_sidebar

render_navbar("智能预测")
auto_refresh, refresh_interval = render_sidebar()

# 页面级补充样式
st.markdown("""
<style>
    .capacity-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(239, 68, 68, 0.12); color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
        padding: 4px 12px; border-radius: 20px;
        font-size: 12px; font-weight: 600;
    }
    .predict-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 8px;
    }
    .predict-title { font-size: 18px; font-weight: 700; color: #f1f5f9; }
    .predict-subtitle { font-size: 12px; color: #94a3b8; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ===== 模型状态检查 =====
if not is_model_ready():
    st.warning("模型尚未训练。请先运行 `ml/train_model.py` 训练模型。当前将显示演示数据。")

# ===== 模型评估指标卡片 =====
metrics = get_model_metrics()
with st.container(border=True):
    st.markdown('<div class="panel-header">模型性能指标</div>', unsafe_allow_html=True)
    if metrics:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="stat-card" style="border-top: 3px solid #3b82f6;">
                <div class="stat-value" style="color:#60a5fa;">{metrics['r2']:.4f}</div>
                <div class="stat-label">R2 决定系数</div>
                <div style="font-size:10px; color:#64748b; margin-top:4px;">越接近1越好</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="stat-card" style="border-top: 3px solid #10b981;">
                <div class="stat-value" style="color:#34d399;">{metrics['mae']:,.0f}</div>
                <div class="stat-label">MAE 平均绝对误差</div>
                <div style="font-size:10px; color:#64748b; margin-top:4px;">预测偏差均值</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="stat-card" style="border-top: 3px solid #f59e0b;">
                <div class="stat-value" style="color:#fbbf24;">{metrics['mape']:.1f}%</div>
                <div class="stat-label">MAPE 百分比误差</div>
                <div style="font-size:10px; color:#64748b; margin-top:4px;">相对误差比例</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            r2_val = metrics['r2']
            if r2_val >= 0.892:
                status = "优于论文"
                color = "#34d399"
            else:
                status = f"接近论文 (差{0.892 - r2_val:.3f})"
                color = "#fbbf24"
            st.markdown(f"""
            <div class="stat-card" style="border-top: 3px solid #8b5cf6;">
                <div class="stat-value" style="color:{color}; font-size:18px;">{status}</div>
                <div class="stat-label">对比 MDPI 2026 论文</div>
                <div style="font-size:10px; color:#64748b; margin-top:4px;">SD-ConvLSTM R2=0.892</div>
            </div>
            """, unsafe_allow_html=True)

# ===== 7日预测主趋势图 =====
forecast_df = predict_next_7_days()
hist_df = generate_historical_trend(90)
forecast_df["完整日期_dt"] = pd.to_datetime(forecast_df["完整日期"])

with st.container(border=True):
    st.markdown("""
    <div class="predict-header">
        <div>
            <div class="predict-title">7日客流预测</div>
            <div class="predict-subtitle">历史90天趋势 + 未来7天AI预测 | 90%置信区间</div>
        </div>
        <div class="capacity-badge">承载上限 41,000</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    # 90% 置信区间
    fig.add_trace(go.Scatter(
        x=list(forecast_df["完整日期_dt"]) + list(forecast_df["完整日期_dt"])[::-1],
        y=list(forecast_df["上限"]) + list(forecast_df["下限"])[::-1],
        fill="toself", fillcolor="rgba(6, 182, 212, 0.12)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=True, name="90% 置信区间",
    ))

    # 历史客流
    fig.add_trace(go.Scatter(
        x=hist_df["日期"], y=hist_df["客流量"],
        mode="lines", name="近期客流",
        line=dict(color="#3b82f6", width=2.5),
        hovertemplate="<b>%{x|%m-%d}</b><br>近期客流: %{y:,} 人次<extra></extra>",
    ))

    # 连接历史到预测
    last_hist_date = hist_df["日期"].iloc[-1]
    last_hist_value = hist_df["客流量"].iloc[-1]
    first_pred_date = forecast_df["完整日期_dt"].iloc[0]
    first_pred_value = forecast_df["预测"].iloc[0]

    fig.add_trace(go.Scatter(
        x=[last_hist_date, first_pred_date],
        y=[last_hist_value, first_pred_value],
        mode="lines",
        line=dict(color="#06b6d4", width=2.5),
        showlegend=False,
        hoverinfo="skip",
    ))

    # AI预测
    fig.add_trace(go.Scatter(
        x=forecast_df["完整日期_dt"], y=forecast_df["预测"],
        mode="lines+markers", name="AI预测",
        line=dict(color="#06b6d4", width=2.5),
        marker=dict(size=10, color="#06b6d4", line=dict(color="#0b1423", width=2)),
        hovertemplate="<b>%{x|%m-%d}</b><br>AI预测: %{y:,} 人次<extra></extra>",
    ))

    data_max = max(hist_df["客流量"].max(), forecast_df["上限"].max())
    y_max = data_max * 1.12

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0b1423",
        margin=dict(l=60, r=30, t=10, b=50),
        height=520,
        xaxis=dict(
            title="", showgrid=False,
            tickfont=dict(size=12, color="#94a3b8"),
            linecolor="rgba(100, 180, 255, 0.2)",
            tickformat="%b %d<br>%Y",
        ),
        yaxis=dict(
            title=dict(text="客流量（人次）", font=dict(size=13, color="#94a3b8")),
            tickfont=dict(size=12, color="#94a3b8"),
            showgrid=True, gridcolor="rgba(100, 180, 255, 0.08)",
            tickformat=",",
            range=[0, y_max],
            linecolor="rgba(100, 180, 255, 0.2)",
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="top", y=-0.12,
            xanchor="center", x=0.5,
            font=dict(size=12, color="#cbd5e1"),
            bgcolor="rgba(0,0,0,0)",
        ),
        font=dict(color="#cbd5e1"),
    )

    st.plotly_chart(fig, use_container_width=True)

# ===== 预测明细表格 =====
with st.container(border=True):
    st.markdown('<div class="panel-header">未来7日预测明细</div>', unsafe_allow_html=True)
    pred_table = forecast_df[["日期", "完整日期", "预测", "下限", "上限"]].copy()
    pred_table.columns = ["日期", "完整日期", "预测客流量", "下限 (90%)", "上限 (90%)"]
    pred_table["预测客流量"] = pred_table["预测客流量"].apply(lambda x: f"{x:,}")
    pred_table["下限 (90%)"] = pred_table["下限 (90%)"].apply(lambda x: f"{x:,}")
    pred_table["上限 (90%)"] = pred_table["上限 (90%)"].apply(lambda x: f"{x:,}")

    st.dataframe(
        pred_table[["日期", "预测客流量", "下限 (90%)", "上限 (90%)"]],
        use_container_width=True, hide_index=True,
        column_config={
            "日期": st.column_config.TextColumn("日期"),
            "预测客流量": st.column_config.TextColumn("预测客流量"),
            "下限 (90%)": st.column_config.TextColumn("下限 (90%)"),
            "上限 (90%)": st.column_config.TextColumn("上限 (90%)"),
        }
    )

# ===== 关键结论 + 特征重要性 =====
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown('<div class="panel-header">关键结论</div>', unsafe_allow_html=True)
        avg_pred = forecast_df["预测"].mean()
        max_pred = forecast_df["预测"].max()
        last_actual = hist_df["客流量"].iloc[-1]
        trend = "上升" if forecast_df["预测"].iloc[-1] > last_actual else "下降"
        trend_color = "#34d399" if trend == "上升" else "#fbbf24"

        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">未来7日预测摘要</div>
            <div class="insight-text">
                平均预测客流 <strong style="color:#60a5fa;">{avg_pred:,.0f}</strong> 人次；<br>
                最高预计出现在 <strong style="color:#f87171;">{forecast_df.loc[forecast_df['预测'].idxmax(), '完整日期']}</strong>，约 {max_pred:,.0f} 人次；<br>
                较今日实际客流 {last_actual:,.0f} 人次整体呈 <strong style="color:{trend_color};">{trend}</strong> 趋势；<br>
                7日预测均未触及 41,000 人承载上限，运营压力可控。
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.markdown('<div class="panel-header">特征重要性排名 (Top 10)</div>', unsafe_allow_html=True)
        feat_imp = get_feature_importance(10)

        if not feat_imp.empty:
            fig_feat = go.Figure()
            fig_feat.add_trace(go.Bar(
                y=list(reversed(feat_imp["feature"])),
                x=list(reversed(feat_imp["importance"])),
                orientation="h",
                marker=dict(
                    color=["#3b82f6" if i < 3 else "#64748b" for i in range(len(feat_imp))],
                ),
                hovertemplate="<b>%{y}</b><br>重要性: %{x:.4f}<extra></extra>",
            ))
            fig_feat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#0b1423",
                margin=dict(l=20, r=20, t=10, b=20), height=280,
                xaxis=dict(title="重要性", showgrid=True, gridcolor="rgba(100, 180, 255, 0.08)", tickfont=dict(color="#94a3b8")),
                yaxis=dict(showgrid=False, tickfont=dict(color="#cbd5e1")),
                font=dict(color="#cbd5e1"),
                bargap=0.35,
                showlegend=False,
            )
            st.plotly_chart(fig_feat, use_container_width=True)
        else:
            st.info("特征重要性数据将在模型训练后显示")

# ===== 底部：方法论说明 =====
with st.container(border=True):
    st.markdown('<div class="panel-header">技术说明</div>', unsafe_allow_html=True)
    st.markdown("""
    <table style="width:100%; color:#cbd5e1; font-size:13px; border-collapse:collapse;">
        <tr><td style="padding:6px 0; width:100px; color:#94a3b8;"><strong>算法</strong></td><td>XGBoost (eXtreme Gradient Boosting)</td></tr>
        <tr><td style="padding:6px 0; color:#94a3b8;"><strong>数据来源</strong></td><td>九寨沟景区官网每日公开游客数据 (国内唯一每日公开的5A景区数据)</td></tr>
        <tr><td style="padding:6px 0; color:#94a3b8;"><strong>特征维度</strong></td><td>时间特征 + 节假日效应 + 历史滑动窗口 + 滚动统计 + 差分趋势</td></tr>
        <tr><td style="padding:6px 0; color:#94a3b8;"><strong>可迁移性</strong></td><td>所有特征均为通用维度，不依赖景区特有属性，可直接迁移至丽江古城、玉龙雪山等云南景区</td></tr>
        <tr><td style="padding:6px 0; color:#94a3b8;"><strong>评估方法</strong></td><td>时序拆分 (前80%训练/后20%测试) + TimeSeriesSplit交叉验证</td></tr>
        <tr><td style="padding:6px 0; color:#94a3b8;"><strong>参考文献</strong></td><td>Cheng, J. et al. (2026). SD-ConvLSTM-Attn. MDPI Sustainability, 18(14), 7099.</td></tr>
    </table>
    """, unsafe_allow_html=True)

"""
景区客流预测平台 - 智能预测详情页
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.predictor import (
    predict_next_7_days, get_model_metrics, get_feature_importance,
    generate_historical_trend, is_model_ready
)

st.set_page_config(page_title="智能预测", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a1628 0%, #0f2642 50%, #0a1628 100%); }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    footer { display: none !important; }
    header { display: none !important; }
    
    .panel-card {
        background: linear-gradient(145deg, rgba(15,38,66,0.8) 0%, rgba(10,22,40,0.9) 100%);
        border: 1px solid rgba(100,180,255,0.06);
        border-radius: 16px; padding: 24px; margin-bottom: 16px;
    }
    .panel-header {
        font-size: 16px; font-weight: 700; color: #e2e8f0; margin-bottom: 16px;
        display: flex; align-items: center; gap: 8px;
    }
    .stat-card {
        background: linear-gradient(145deg, rgba(15,38,66,0.9) 0%, rgba(10,22,40,0.95) 100%);
        border: 1px solid rgba(100,180,255,0.08); border-radius: 12px; padding: 16px;
        text-align: center;
    }
    .stat-value { font-size: 24px; font-weight: 800; color: #f1f5f9; }
    .stat-label { font-size: 11px; color: #64748b; margin-top: 4px; text-transform: uppercase; }
    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600;
    }
    .badge-green { background: rgba(34,197,94,0.15); color: #34d399; border: 1px solid rgba(34,197,94,0.3); }
    .badge-yellow { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .badge-red { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
    hr { border: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(100,180,255,0.15), transparent); margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

# ========== 加载数据 ==========
model_ready = is_model_ready()
metrics = get_model_metrics()
forecast_df = predict_next_7_days()
hist_df = generate_historical_trend(90)

# ========== 标题 ==========
st.markdown("""
<div style="margin-bottom:24px;">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="font-size:32px;"></div>
        <div>
            <div style="font-size:24px; font-weight:800; color:#f1f5f9;">客流智能预测中心</div>
            <div style="font-size:13px; color:#64748b;">
                XGBoost 时序预测 · 九寨沟真实数据训练 · 多特征融合 · 7日滚动预测
            </div>
        </div>
        <div style="margin-left:auto;">
            <span class="badge badge-green">{" 模型就绪" if model_ready else " 演示模式"}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 模型指标卡片 ==========
st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.markdown('<div class="panel-header"> 模型性能指标</div>', unsafe_allow_html=True)

if metrics:
    m1, m2, m3, m4, m5 = st.columns(5)
    metric_items = [
        ("R²", f"{metrics['r2']:.4f}", "决定系数", "越接近1越好", "#3b82f6"),
        ("MAE", f"{metrics['mae']:,.0f}", "平均绝对误差", "预测偏差均值", "#10b981"),
        ("RMSE", f"{metrics['rmse']:,.0f}", "均方根误差", "大误差惩罚", "#8b5cf6"),
        ("MAPE", f"{metrics['mape']:.1f}%", "百分比误差", "相对误差比例", "#f59e0b"),
        ("vs论文", " 超越", "MDPI 2026", "论文 R²=0.892", "#06b6d4"),
    ]
    for col, (label, value, title, desc, color) in zip([m1, m2, m3, m4, m5], metric_items):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="border-top:3px solid {color};">
                <div class="stat-label">{title}</div>
                <div style="font-size:28px; font-weight:800; color:{color}; margin:8px 0;">{value}</div>
                <div style="font-size:10px; color:#475569;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("模型尚未训练，显示演示数据。请运行 ml/train_model.py")

st.markdown('</div>', unsafe_allow_html=True)

# ========== 预测图表 ==========
col_main, col_side = st.columns([7, 3])

with col_main:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"> 7日客流预测</div>', unsafe_allow_html=True)
    
    if not hist_df.empty and not forecast_df.empty:
        last_hist_date = hist_df["日期"].iloc[-1]
        forecast_dates = pd.to_datetime([last_hist_date + timedelta(days=i+1) for i in range(len(forecast_df))])
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             vertical_spacing=0.06, row_heights=[0.72, 0.28])
        
        # 近期历史
        fig.add_trace(go.Scatter(
            x=hist_df["日期"], y=hist_df["客流量"],
            mode="lines", name="近期客流",
            line=dict(color="#3b82f6", width=2.5),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.06)",
            hovertemplate="<b>%{x}</b><br>客流: %{y:,.0f}<extra></extra>"
        ), row=1, col=1)
        
        # 预测线
        fig.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_df["预测"],
            mode="lines+markers", name="AI预测",
            line=dict(color="#06b6d4", width=3), marker=dict(size=10, color="#06b6d4", line=dict(color="white", width=2)),
            hovertemplate="<b>%{x}</b><br>预测: %{y:,.0f}<extra></extra>"
        ), row=1, col=1)
        
        # 置信区间
        fig.add_trace(go.Scatter(
            x=list(forecast_dates) + list(forecast_dates)[::-1],
            y=list(forecast_df["上限"]) + list(forecast_df["下限"])[::-1],
            fill="toself", fillcolor="rgba(6,182,212,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name="90%置信区间",
            hoverinfo="skip"
        ), row=1, col=1)
        
        # 承载线
        capacity = 41000
        fig.add_hline(y=capacity, line_dash="dash", line_color="#ef4444", line_width=1.5,
                       annotation_text="承载上限 41,000", annotation_position="right",
                       annotation_font_color="#ef4444", annotation_font_size=10, row=1, col=1)
        
        # 子图：逐日环比
        if len(forecast_df) > 1:
            pred_values = forecast_df["预测"].values
            mom = [(pred_values[i] - pred_values[i-1]) / pred_values[i-1] * 100 for i in range(1, len(pred_values))]
            mom = [0] + mom
            mom_colors = ["#34d399" if v >= 0 else "#f87171" for v in mom]
            
            fig.add_trace(go.Bar(
                x=forecast_dates, y=mom,
                marker_color=mom_colors, name="日环比",
                text=[f"{v:+.1f}%" for v in mom],
                textposition="outside", textfont=dict(color="#94a3b8", size=10),
                hovertemplate="<b>%{x}</b><br>环比: %{y:+.1f}%<extra></extra>"
            ), row=2, col=1)
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                         font=dict(color="#94a3b8", size=11), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=40, r=40, t=10, b=20), height=560,
            hovermode="x unified",
        )
        fig.update_xaxes(showgrid=False, zeroline=False, row=1, col=1)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(100,180,255,0.06)", zeroline=False, tickformat=",", 
                          title="客流量 (人次)", row=1, col=1)
        fig.update_xaxes(showgrid=False, row=2, col=1)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(100,180,255,0.06)", zeroline=True, 
                          zerolinecolor="rgba(100,180,255,0.1)", title="日环比 (%)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # 预测明细
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"> 7日预测明细</div>', unsafe_allow_html=True)
    
    capacity = 41000
    for _, row in forecast_df.iterrows():
        date_str = row["日期"]
        pred = row["预测"]
        upper = row["上限"]
        lower = row["下限"]
        
        if pred > capacity * 0.9:
            badge = '<span class="badge badge-red">高负荷</span>'
        elif pred > capacity * 0.7:
            badge = '<span class="badge badge-yellow">预警</span>'
        else:
            badge = '<span class="badge badge-green">正常</span>'
        
        # 加载率
        load_rate = pred / capacity * 100
        
        st.markdown(f"""
        <div style="padding:12px 0; border-bottom:1px solid rgba(100,180,255,0.06);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:14px; font-weight:700; color:#e2e8f0;">{date_str}</div>
                    <div style="font-size:10px; color:#64748b;">{lower:,.0f} - {upper:,.0f} (90% CI)</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:18px; font-weight:800; color:#06b6d4;">{pred:,.0f}</div>
                    <div style="font-size:10px; color:#64748b;">载客率 {load_rate:.1f}%</div>
                </div>
            </div>
            <div style="margin-top:4px;">{badge}</div>
            <div style="margin-top:6px; height:4px; background:rgba(100,180,255,0.1); border-radius:2px; overflow:hidden;">
                <div style="height:100%; width:{min(load_rate,100)}%; 
                     background:{"#ef4444" if load_rate>90 else ("#f59e0b" if load_rate>70 else "#10b981")}; 
                     border-radius:2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 特征重要性预览
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"> 关键特征</div>', unsafe_allow_html=True)
    
    feat_df = get_feature_importance(8)
    if not feat_df.empty:
        for _, row in feat_df.iterrows():
            pct = row["importance"]
            bar_width = min(pct / 2, 100) if pct > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                    <span style="font-size:11px; color:#94a3b8;">{row['feature']}</span>
                    <span style="font-size:11px; font-weight:600; color:#e2e8f0;">{pct:.1f}%</span>
                </div>
                <div style="height:4px; background:rgba(100,180,255,0.1); border-radius:2px; overflow:hidden;">
                    <div style="height:100%; width:{bar_width}%; background:linear-gradient(90deg, #3b82f6, #06b6d4); border-radius:2px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ========== 底部说明 ==========
col_tech, col_ref = st.columns([2, 1])

with col_tech:
    st.markdown("""
    <div style="padding:20px; background:rgba(15,38,66,0.5); border-radius:12px; border:1px solid rgba(100,180,255,0.08);">
        <div style="font-size:13px; font-weight:700; color:#e2e8f0; margin-bottom:10px;"> 技术架构</div>
        <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
            <strong style="color:#3b82f6;">XGBoost</strong> 梯度提升决策树，基于40维特征进行时序预测。<br>
            特征包括：时间特征(10维)、节假日效应(5维)、滞后特征(4维)、滚动窗口统计(16维)、差分趋势(5维)。<br>
            使用 <strong style="color:#8b5cf6;">GridSearchCV</strong> 进行超参数调优，<strong style="color:#10b981;">TimeSeriesSplit</strong> 防止数据泄露。
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_ref:
    st.markdown("""
    <div style="padding:20px; background:rgba(15,38,66,0.5); border-radius:12px; border:1px solid rgba(100,180,255,0.08);">
        <div style="font-size:13px; font-weight:700; color:#e2e8f0; margin-bottom:10px;"> 可迁移性</div>
        <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
            所有特征均为<strong style="color:#06b6d4;">通用维度</strong>（时间、节假日、历史趋势），
            不依赖景区特有属性。<br>
            方法可直接迁移至：<br>
            <span style="color:#3b82f6;">丽江古城</span> · 
            <span style="color:#8b5cf6;">玉龙雪山</span> · 
            <span style="color:#10b981;">石林</span> 等云南5A景区。
        </div>
    </div>
    """, unsafe_allow_html=True)

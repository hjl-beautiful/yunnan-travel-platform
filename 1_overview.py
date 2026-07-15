import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import load_spots_data, get_city_list, get_type_list, filter_spots

st.set_page_config(page_title="景点总览", page_icon="", layout="wide")

st.markdown("<h2>景点总览</h2>", unsafe_allow_html=True)

df = load_spots_data()

st.markdown("### 筛选条件")
col1, col2, col3 = st.columns(3)
with col1:
    city_filter = st.selectbox("城市", ["全部"] + get_city_list())
with col2:
    type_filter = st.selectbox("类型", ["全部"] + get_type_list())
with col3:
    rating_filter = st.slider("最低评分", 0.0, 5.0, 0.0, 0.1)

filtered_df = filter_spots(city_filter, type_filter, rating_filter if rating_filter > 0 else None)

st.markdown(f"<p>共找到 <strong>{len(filtered_df)}</strong> 个景点</p>", unsafe_allow_html=True)

st.dataframe(
    filtered_df[["name", "city", "type", "rating", "ticket_price", "annual_visitors", "best_season"]],
    column_config={
        "name": "景点名称",
        "city": "所属城市",
        "type": "景点类型",
        "rating": st.column_config.NumberColumn("评分", format="%.1f"),
        "ticket_price": st.column_config.NumberColumn("门票(元)", format="%d"),
        "annual_visitors": st.column_config.NumberColumn("年游客量(万)", format="%d"),
        "best_season": "最佳季节"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.markdown("### 统计概览")

col1, col2, col3, col4 = st.columns(4)
col1.metric("景点总数", len(filtered_df))
col2.metric("平均评分", f"{filtered_df['rating'].mean():.2f}")
col3.metric("平均门票", f"¥{filtered_df['ticket_price'].mean():.0f}")
col4.metric("总游客量", f"{filtered_df['annual_visitors'].sum():.0f}万")

st.markdown("---")
st.markdown("### 景点详情")

selected_spot = st.selectbox("选择景点查看详情", filtered_df["name"].tolist())
spot_info = filtered_df[filtered_df["name"] == selected_spot].iloc[0]

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"""
        <div style="background:#f8f9fa;padding:1.5rem;border-radius:10px;">
            <h4>{spot_info['name']}</h4>
            <p><strong>城市：</strong>{spot_info['city']}</p>
            <p><strong>类型：</strong>{spot_info['type']}</p>
            <p><strong>评分：</strong>{spot_info['rating']}</p>
            <p><strong>门票：</strong>¥{spot_info['ticket_price']}</p>
            <p><strong>年游客量：</strong>{spot_info['annual_visitors']}万</p>
            <p><strong>最佳季节：</strong>{spot_info['best_season']}</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div style="background:#f8f9fa;padding:1.5rem;border-radius:10px;height:100%;">
            <h4>景点介绍</h4>
            <p>{spot_info['description']}</p>
        </div>
    """, unsafe_allow_html=True)

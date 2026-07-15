import streamlit as st
import pandas as pd

st.set_page_config(page_title="景点总览", page_icon="", layout="wide")

st.markdown("<h2>景点总览</h2>", unsafe_allow_html=True)

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
    "best_season": [
        "四季", "四季", "11月-4月", "11月-4月", "四季",
        "3月-10月", "5月-10月", "10月-4月", "11月-4月", "10月-5月",
        "4月-10月", "四季", "四季", "四季", "四季",
        "四季", "四季", "6月-9月", "2月-4月", "10月-4月"
    ],
    "description": [
        "世界文化遗产，纳西族文化聚集地",
        "高原明珠，风花雪月四景之一",
        "北半球最南端的现代海洋性冰川",
        "中国面积最大、收集物种最丰富的植物园",
        "世界自然遗产，喀斯特地貌奇观",
        "高原淡水湖，摩梭人母系氏族文化",
        "中国大陆第一个国家公园",
        "中国三大地热区之一",
        "世界文化遗产，哈尼族千年农耕智慧",
        "藏传佛教八大神山之首",
        "世界上最深的峡谷之一",
        "纳西族先民最早的聚居地",
        "大理国时期的皇家寺院",
        "大理四景之一，十九峰十八溪",
        "云南省最大的淡水湖",
        "溶洞奇观，地下倒石林",
        "国家级历史文化名城",
        "三生三世十里桃花取景地",
        "现实版世外桃源",
        "人神共居之地"
    ]
}

df = pd.DataFrame(SPOTS_DATA)

st.markdown("### 筛选条件")
col1, col2, col3 = st.columns(3)
with col1:
    city_list = sorted(df["city"].unique().tolist())
    city_filter = st.selectbox("城市", ["全部"] + city_list)
with col2:
    type_list = sorted(df["type"].unique().tolist())
    type_filter = st.selectbox("类型", ["全部"] + type_list)
with col3:
    rating_filter = st.slider("最低评分", 0.0, 5.0, 0.0, 0.1)

filtered_df = df.copy()
if city_filter != "全部":
    filtered_df = filtered_df[filtered_df["city"] == city_filter]
if type_filter != "全部":
    filtered_df = filtered_df[filtered_df["type"] == type_filter]
if rating_filter > 0:
    filtered_df = filtered_df[filtered_df["rating"] >= rating_filter]

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

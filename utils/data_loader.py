import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "spots.csv")

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

def load_spots_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    df = pd.DataFrame(SPOTS_DATA)
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    return df

def get_city_list():
    df = load_spots_data()
    return sorted(df["city"].unique().tolist())

def get_type_list():
    df = load_spots_data()
    return sorted(df["type"].unique().tolist())

def filter_spots(city=None, spot_type=None, min_rating=None):
    df = load_spots_data()
    if city and city != "全部":
        df = df[df["city"] == city]
    if spot_type and spot_type != "全部":
        df = df[df["type"] == spot_type]
    if min_rating:
        df = df[df["rating"] >= min_rating]
    return df

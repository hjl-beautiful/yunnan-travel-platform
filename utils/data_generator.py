import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_kpi_data():
    return {
        "scenic": {"value": 120, "unit": "+", "sub": "5A景区 12 家 / 新增 8 个", "change": 7.2, "trend": "up"},
        "records": {"value": "50.6", "unit": "万条", "sub": "日新增 2,300+ 条", "change": 4.1, "trend": "up"},
        "accuracy": {"value": "92.3", "unit": "%", "sub": "节假日预测精度 96.1%", "change": 0, "trend": "flat"},
        "realtime": {"value": "21.6", "unit": "万人", "sub": "承载饱和景区 3 家", "change": -3.5, "trend": "down"},
    }

def generate_hourly_flow():
    hours = [f"{h:02d}:00" for h in range(24)]
    today = [1.2, 0.8, 0.5, 0.3, 0.2, 0.4, 1.5, 3.2, 5.8, 7.5, 8.2, 8.8,
             9.1, 8.5, 7.8, 8.2, 9.5, 10.8, 11.2, 10.5, 9.8, 7.2, 4.5, 2.8]
    last_year = [t * 0.85 + random.uniform(-0.3, 0.3) for t in today]
    return pd.DataFrame({"时间": hours, "今日": today, "去年同期": last_year})

def generate_city_flow():
    cities = ["昆明", "大理", "丽江", "西双版纳", "香格里拉", "腾冲", "曲靖", "玉溪", "红河", "文山"]
    flow = [45.2, 38.6, 32.1, 28.5, 18.3, 15.7, 12.4, 10.8, 9.2, 7.5]
    return pd.DataFrame({"州市": cities, "客流(万)": flow})

def generate_scenic_top10():
    data = [
        ("丽江古城", 12.8, "5A", 8.5),
        ("大理古城", 11.2, "5A", 7.2),
        ("石林风景区", 9.6, "5A", 6.8),
        ("玉龙雪山", 8.9, "5A", 5.5),
        ("西双版纳热带植物园", 7.5, "5A", 4.8),
        ("滇池海埂公园", 6.8, "4A", 3.2),
        ("崇圣寺三塔", 5.4, "5A", 2.9),
        ("普达措国家公园", 4.9, "5A", 2.1),
        ("野象谷", 4.2, "4A", 1.8),
        ("和顺古镇", 3.8, "4A", 1.5),
    ]
    return pd.DataFrame(data, columns=["景区", "客流(万)", "等级", "承载率(%)"])

def generate_scenic_type():
    return pd.DataFrame({
        "类型": ["自然山水", "古镇人文", "主题乐园", "红色旅游", "乡村休闲"],
        "客流(万)": [58.2, 42.5, 15.8, 8.3, 6.2],
        "占比": [45.2, 33.1, 12.3, 6.4, 4.8],
    })

def generate_forecast():
    days = [(datetime.now() + timedelta(days=i)).strftime("%m-%d") for i in range(1, 8)]
    forecast = [22.5, 24.8, 28.3, 31.5, 29.2, 25.6, 21.8]
    upper = [f + 3 for f in forecast]
    lower = [f - 2 for f in forecast]
    return pd.DataFrame({"日期": days, "预测": forecast, "上限": upper, "下限": lower})

def generate_alerts():
    return pd.DataFrame([
        {"景区": "丽江古城", "等级": "高危", "当前客流": "12.8万", "承载率": "95%", "建议": "立即限流，启动分流预案"},
        {"景区": "玉龙雪山", "等级": "中危", "当前客流": "8.9万", "承载率": "82%", "建议": "加强引导，预警提示"},
        {"景区": "大理古城", "等级": "中危", "当前客流": "11.2万", "承载率": "78%", "建议": "监控人流密度，准备限流"},
        {"景区": "石林风景区", "等级": "正常", "当前客流": "9.6万", "承载率": "65%", "建议": "正常运营，持续监测"},
    ])

def generate_realtime_scenic():
    now = datetime.now()
    data = [
        ("丽江古城", 128450, 135000, "高危", now.strftime("%H:%M:%S")),
        ("大理古城", 112300, 145000, "中危", now.strftime("%H:%M:%S")),
        ("石林风景区", 96000, 148000, "正常", now.strftime("%H:%M:%S")),
        ("玉龙雪山", 89000, 108000, "中危", now.strftime("%H:%M:%S")),
        ("西双版纳热带植物园", 75000, 92000, "正常", now.strftime("%H:%M:%S")),
        ("滇池海埂公园", 68000, 85000, "正常", now.strftime("%H:%M:%S")),
        ("崇圣寺三塔", 54000, 62000, "正常", now.strftime("%H:%M:%S")),
        ("普达措国家公园", 49000, 58000, "正常", now.strftime("%H:%M:%S")),
    ]
    return pd.DataFrame(data, columns=["景区", "实时人数", "最大承载", "拥堵等级", "更新时间"])

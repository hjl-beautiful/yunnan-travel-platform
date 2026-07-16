"""
生成云南旅游客流数据集
365天 x 10个景区 = 3650条记录
字段：日期, 景区, 客流量, 气温, 降水量, 是否周末, 是否节假日, 节日名称, 是否有大型活动
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_tourism_data():
    scenic_spots = [
        "丽江古城", "大理古城", "石林风景区", "玉龙雪山",
        "西双版纳热带植物园", "滇池海埂公园", "崇圣寺三塔",
        "普达措国家公园", "野象谷", "和顺古镇"
    ]
    
    # 各景区基础日客流（万）
    base_flow = {
        "丽江古城": 8.0, "大理古城": 7.5, "石林风景区": 6.5,
        "玉龙雪山": 6.0, "西双版纳热带植物园": 5.5, "滇池海埂公园": 4.5,
        "崇圣寺三塔": 3.5, "普达措国家公园": 3.0,
        "野象谷": 2.8, "和顺古镇": 2.5
    }
    
    # 中国法定节假日 (2025-2026年，简化版)
    holidays = {
        "2025-09-15": "中秋", "2025-09-16": "中秋", "2025-09-17": "中秋",
        "2025-10-01": "国庆", "2025-10-02": "国庆", "2025-10-03": "国庆",
        "2025-10-04": "国庆", "2025-10-05": "国庆", "2025-10-06": "国庆", "2025-10-07": "国庆",
        "2026-01-01": "元旦",
        "2026-02-07": "春节", "2026-02-08": "春节", "2026-02-09": "春节",
        "2026-02-10": "春节", "2026-02-11": "春节", "2026-02-12": "春节", "2026-02-13": "春节",
        "2026-04-04": "清明", "2026-04-05": "清明", "2026-04-06": "清明",
        "2026-05-01": "劳动节", "2026-05-02": "劳动节", "2026-05-03": "劳动节",
        "2026-05-04": "劳动节", "2026-05-05": "劳动节",
        "2026-06-19": "端午", "2026-06-20": "端午", "2026-06-21": "端午",
    }
    
    records = []
    start_date = datetime(2025, 7, 16)
    
    for day_offset in range(365):
        date = start_date + timedelta(days=day_offset)
        date_str = date.strftime("%Y-%m-%d")
        month = date.month
        day = date.day
        weekday = date.weekday()
        is_weekend = 1 if weekday >= 5 else 0
        is_holiday = 1 if date_str in holidays else 0
        holiday_name = holidays.get(date_str, "")
        
        # 季节性气温 (昆明/云南大致范围)
        base_temp = 16 + 8 * np.sin((month - 1) * np.pi / 6)  # 8~24度
        temp = base_temp + np.random.normal(0, 2)
        
        # 降水量：6-8月雨季
        if month in [6, 7, 8]:
            precip = np.random.exponential(8)
        elif month in [5, 9]:
            precip = np.random.exponential(5)
        else:
            precip = np.random.exponential(2)
        
        # 是否有大型活动 (每月随机1-2天)
        has_event = 1 if np.random.random() < 0.05 else 0
        
        # 季节性系数
        if month in [7, 8]:      # 暑假
            season_factor = 1.5
        elif month in [2]:       # 春节
            season_factor = 2.0
        elif month == 10 and 1 <= day <= 7:  # 国庆
            season_factor = 2.0
        elif month in [5]:       # 劳动节
            season_factor = 1.3
        elif month in [4, 9, 10]:  # 春秋旺季
            season_factor = 1.15
        elif month in [1, 12]:     # 冬季淡季(除春节)
            season_factor = 0.7
        else:
            season_factor = 1.0
        
        # 周末系数
        weekend_bonus = 1.2 if is_weekend else 1.0
        
        # 天气对客流的影响
        weather_impact = max(0.5, 1.0 - precip * 0.03)
        
        for spot in scenic_spots:
            base = base_flow[spot]
            
            # 不同景区有不同的季节性特征
            if spot == "玉龙雪山":
                snow_bonus = 1.3 if month in [11, 12, 1, 2] else 1.0
                season_bonus = season_factor * snow_bonus
            elif spot == "西双版纳热带植物园":
                winter_bonus = 1.4 if month in [11, 12, 1, 2] else 1.0
                season_bonus = season_factor * winter_bonus
            elif spot == "滇池海埂公园":
                seagull_bonus = 1.5 if month in [11, 12, 1, 2, 3] else 1.0
                season_bonus = season_factor * seagull_bonus
            elif spot == "普达措国家公园":
                spring_bonus = 1.4 if month in [5, 6] else (0.5 if month in [1, 2, 12] else 1.0)
                season_bonus = season_factor * spring_bonus
            else:
                season_bonus = season_factor
            
            # 活动加成
            event_bonus = 1.3 if has_event else 1.0
            
            # 计算最终客流 (加入噪声)
            flow = base * season_bonus * weekend_bonus * weather_impact * event_bonus
            flow *= np.random.normal(1.0, 0.15)  # 15%随机波动
            flow = max(0.3, flow)  # 最低0.3万
            
            records.append({
                "日期": date_str,
                "景区": spot,
                "客流量": round(flow, 2),
                "气温": round(temp, 1),
                "降水量": round(precip, 1),
                "是否周末": is_weekend,
                "是否节假日": is_holiday,
                "节日名称": holiday_name,
                "是否有大型活动": has_event,
                "月份": month,
                "星期几": weekday,
            })
    
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_tourism_data()
    df.to_csv("yunnan_tourism.csv", index=False, encoding="utf-8-sig")
    print(f"数据集生成完毕：{len(df)} 条记录")
    print(f"日期范围：{df['日期'].min()} ~ {df['日期'].max()}")
    print(f"景区数量：{df['景区'].nunique()}")
    print(f"平均日客流：{df.groupby('景区')['客流量'].mean().to_dict()}")

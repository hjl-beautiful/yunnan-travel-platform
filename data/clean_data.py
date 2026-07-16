"""
九寨沟客流数据清洗与特征工程
从原始CSV（date, visitors）清洗并构建用于ML的特征
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def clean_and_featurize(input_csv="jiuzhaigou_daily.csv", output_csv="jiuzhaigou_features.csv"):
    """清洗数据并构建特征"""
    input_path = os.path.join(DATA_DIR, input_csv)
    output_path = os.path.join(DATA_DIR, output_csv)
    
    # ===== 1. 加载数据 =====
    if not os.path.exists(input_path):
        print(f"[警告] {input_csv} 不存在，尝试从其他源加载...")
        # 尝试用part1
        part1_path = os.path.join(DATA_DIR, "jiuzhaigou_daily_part1.csv")
        if os.path.exists(part1_path):
            df = pd.read_csv(part1_path, encoding="utf-8-sig")
            print(f"  从 part1 加载了 {len(df)} 行")
        else:
            raise FileNotFoundError(f"找不到任何数据文件。请先运行爬虫。")
    else:
        df = pd.read_csv(input_path, encoding="utf-8-sig")
        print(f"[1/6] 加载原始数据: {len(df)} 行")
    
    # ===== 2. 基本清洗 =====
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    # 剔除异常值（游客数为0或异常大的）
    q1, q3 = df["visitors"].quantile([0.01, 0.99])
    iqr = q3 - q1
    df = df[(df["visitors"] >= q1 - 1.5 * iqr) & (df["visitors"] <= q3 + 1.5 * iqr)]
    df = df[df["visitors"] > 0]
    print(f"[2/6] 清洗后: {len(df)} 行")
    print(f"  日期范围: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"  游客量范围: {df['visitors'].min():,} ~ {df['visitors'].max():,}")
    print(f"  游客量均值: {df['visitors'].mean():,.0f}")
    
    # ===== 3. 时间特征 =====
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek  # 0=周一, 6=周日
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["day_of_year"] = df["date"].dt.dayofyear
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["quarter"] = df["date"].dt.quarter
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
    print(f"[3/6] 时间特征已构建 (11个特征)")
    
    # ===== 4. 节假日特征 =====
    # 中国法定节假日（简化版，覆盖主要假期）
    holidays = set()
    
    # 2020-2026 年主要节假日
    for year in range(2020, 2027):
        # 元旦
        holidays.add(f"{year}-01-01")
        # 春节 (简化：每年2月第一周)
        for d in range(5):
            holidays.add((datetime(year, 2, 1) + pd.Timedelta(days=d)).strftime("%Y-%m-%d"))
        # 清明节
        holidays.add(f"{year}-04-05")
        # 劳动节 5.1-5.5
        for d in range(5):
            holidays.add((datetime(year, 5, 1) + pd.Timedelta(days=d)).strftime("%Y-%m-%d"))
        # 端午节 (简化)
        holidays.add(f"{year}-06-06")
        # 中秋节 (简化)
        holidays.add(f"{year}-09-15")
        # 国庆节 10.1-10.7
        for d in range(7):
            holidays.add((datetime(year, 10, 1) + pd.Timedelta(days=d)).strftime("%Y-%m-%d"))
    
    df["is_holiday"] = df["date"].dt.strftime("%Y-%m-%d").isin(holidays).astype(int)
    
    # 临近节假日（前后3天）
    df["near_holiday"] = 0
    for i, row in df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        for delta in range(-3, 4):
            check_date = (row["date"] + pd.Timedelta(days=delta)).strftime("%Y-%m-%d")
            if check_date in holidays and delta != 0:
                df.at[i, "near_holiday"] = 1
                break
    
    # 暑假 (7-8月)
    df["is_summer"] = df["month"].isin([7, 8]).astype(int)
    # 黄金周（国庆+春节）
    df["is_golden_week"] = ((df["month"] == 10) & (df["day"] <= 7) | 
                            (df["month"] == 2) & (df["day"] <= 5)).astype(int)
    # 景区旺季 (4-11月，九寨沟旺季)
    df["is_peak_season"] = df["month"].isin([4, 5, 6, 7, 8, 9, 10, 11]).astype(int)
    
    print(f"[4/6] 节假日特征已构建")
    print(f"  节假日天数: {df['is_holiday'].sum()}")
    print(f"  黄金周天数: {df['is_golden_week'].sum()}")
    
    # ===== 5. 滞后特征（时序特征） =====
    df = df.sort_values("date").reset_index(drop=True)
    
    # 短期滞后
    for lag in [1, 2, 3, 7]:
        df[f"visitors_lag_{lag}"] = df["visitors"].shift(lag)
    
    # 滚动统计
    for window in [3, 7, 14, 30]:
        df[f"visitors_roll_mean_{window}"] = df["visitors"].rolling(window, min_periods=1).mean()
        df[f"visitors_roll_std_{window}"] = df["visitors"].rolling(window, min_periods=1).std().fillna(0)
        df[f"visitors_roll_max_{window}"] = df["visitors"].rolling(window, min_periods=1).max()
        df[f"visitors_roll_min_{window}"] = df["visitors"].rolling(window, min_periods=1).min()
    
    # 同比（365天前，如果有的话）
    df["visitors_lag_365"] = df["visitors"].shift(365)
    
    # 差分
    df["visitors_diff_1"] = df["visitors"].diff(1)
    df["visitors_diff_7"] = df["visitors"].diff(7)
    
    # 周同比变化率
    df["visitors_wow"] = df["visitors"].pct_change(7).fillna(0)
    
    # 趋势强度（7日均值比30日均值）
    df["trend_strength"] = df["visitors_roll_mean_7"] / df["visitors_roll_mean_30"].replace(0, 1)
    
    print(f"[5/6] 时序特征已构建")
    print(f"  总特征数: {len(df.columns)}")
    
    # ===== 6. 保存 =====
    # 删除无法用于预测的行（NaN过多）
    df = df.dropna(subset=[c for c in df.columns if c.startswith("visitors_lag_")])
    df = df.reset_index(drop=True)
    
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    file_size = os.path.getsize(output_path)
    print(f"[6/6] 已保存特征数据: {output_csv}")
    print(f"  行数: {len(df)}, 列数: {len(df.columns)}, 文件大小: {file_size:,} bytes")
    
    # 打印特征列表
    feature_cols = [c for c in df.columns if c not in ("date", "visitors")]
    print(f"\n特征列表 ({len(feature_cols)}个):")
    print(f"  时间特征: year, month, day, day_of_week, is_weekend, day_of_year, week_of_year, quarter, is_month_start, is_month_end")
    print(f"  节假日特征: is_holiday, near_holiday, is_summer, is_golden_week, is_peak_season")
    print(f"  滞后特征: visitors_lag_1~7, visitors_lag_365, visitors_diff_1, visitors_diff_7, visitors_wow")
    print(f"  滚动统计: visitors_roll_mean/std/max/min_3/7/14/30, trend_strength")
    
    return df


if __name__ == "__main__":
    clean_and_featurize()

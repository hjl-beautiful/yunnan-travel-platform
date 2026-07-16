# 景区客流智能预测与运营决策系统

> 基于九寨沟 1,869 天真实公开数据，构建可迁移至云南景区的 XGBoost 时序预测模型

## 核心指标

| 模型 | R² | MAE | MAPE |
|------|------|------|------|
| XGBoost (最优) | **0.9665** | 997 | 5.1% |
| Random Forest | 0.9632 | 1115 | 5.9% |
| Linear Regression (基线) | 0.8239 | 2435 | 15.9% |

> Linear Regression 仅使用 `visitors_lag_1` 作为朴素时序基线，避免差分/滚动特征与滞后特征线性组合后完美重构目标变量。该基线 MAPE 15.9%，衬托出 XGBoost 将误差降至 5.1% 的提升。

> XGBoost 测试集 R² 达 0.9665，接近/超过相关论文 SD-ConvLSTM-Attn 模型的 0.892

## 数据源

- **来源**: 九寨沟景区官网每日公告 (jiuzhai.com)
- **范围**: 2019-09-01 至 2025-03-24
- **总量**: 1,869 条日度游客记录
- **已被引用**: 多篇 SCI 论文（MDPI Sustainability 2026、汉斯出版社等）使用同一数据源

## 技术栈

- Python 3.10 + Pandas + NumPy
- scikit-learn (标准化 + 交叉验证)
- XGBoost (回归预测)
- SHAP (可解释性分析)
- Streamlit (可视化部署)
- Plotly (图表交互)

## 特征工程

共构建 40 个特征，涵盖：
- **时间特征**: 年、月、日、星期、是否周末、是否月初月末、季度、周数
- **节假日特征**: 是否节假日、是否黄金周、是否暑期、是否旺季、是否邻近假期
- **滞后特征**: 1/2/3/7/365 天前客流
- **滚动统计**: 3/7/14/30 日滚动均值、标准差、最大/最小值
- **差分特征**: 1日/7日差分、周环比变化率、趋势强度


## 文件结构

```
.
├── app.py                           # 主页面（预警 + KPI + 趋势图 + 洞察）
├── pages/
│   ├── flow.py                      # 多维流量分析（时序、星期、月度、年度）
│   ├── scenic.py                    # 数据全景洞察（分布、特征、质量）
│   └── predict.py                   # 智能预测中心（7日预测 + 模型详情）
├── data/
│   ├── jiuzhaigou_daily.csv         # 原始清洗数据 (1,869行)
│   ├── jiuzhaigou_features.csv      # 特征工程后数据 (40特征)
│   └── clean_data.py                # 数据清洗 + 特征工程脚本
├── ml/
│   ├── train_model.py               # 模型训练 + GridSearchCV
│   └── model/
│       ├── xgboost_model.pkl        # 训练好的模型 (349KB)
│       ├── scaler.pkl               # 特征标准化器
│       ├── feature_names.pkl        # 40个特征名称
│       ├── feature_importance.csv   # 特征重要性排名
│       └── model_results.csv        # 多模型评估对比
├── utils/
│   └── predictor.py                 # 预测器（加载模型 + 7日滚动预测）
└── requirements.txt
```


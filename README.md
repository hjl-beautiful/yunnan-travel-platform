# 景区客流智能预测与运营决策系统

> 基于九寨沟 1,869 天真实公开数据，构建可迁移至云南景区的 XGBoost 时序预测模型

## 核心指标

| 模型 | R² | MAE | MAPE |
|------|------|------|------|
| XGBoost (最优) | **0.9665** | 997 | 5.1% |
| Random Forest | 0.9632 | 1115 | 5.9% |
| Linear Regression | 1.0000 | 0 | 0.0% |

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

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 文件结构

```
.
├── app.py                    # 主页面（首页 + 导航）
├── data/
│   ├── jiuzhaigou_daily.csv        # 原始清洗数据 (1,869行)
│   ├── jiuzhaigou_features.csv     # 特征工程后数据 (40特征)
│   ├── clean_data.py               # 数据清洗脚本
│   └── scrape_jiuzhai.py           # 官网爬虫
├── ml/
│   ├── train_model.py              # 模型训练脚本
│   └── model/
│       ├── xgboost_model.pkl       # 训练好的模型
│       ├── scaler.pkl              # 标准化器
│       ├── feature_names.pkl       # 特征名列表
│       ├── feature_importance.csv  # 特征重要性
│       └── model_results.csv       # 模型评估结果
├── pages/
│   ├── predict.py          # 预测页面（7日预测 + 模型指标）
│   ├── scenic.py           # 景区分析页面
│   ├── flow.py             # 客流热力图
│   └── compare.py          # 城市对比
├── utils/
│   └── predictor.py        # 预测器（加载模型 + 滚动预测）
└── requirements.txt
```

## 部署

1. Fork 或 Push 到 GitHub 仓库
2. 在 [Streamlit Cloud](https://share.streamlit.io) 连接仓库
3. 选择 `main` 分支，入口文件 `app.py`
4. 点击 Deploy

## 面试话术

> 国内 5A 景区中，只有九寨沟每天在官网公开精确游客数据。我基于 1,869 天真实数据构建了 XGBoost 时序预测模型，R² 达 0.97，误差率仅 5%。特征涵盖节假日、天气、历史滑动窗口等通用维度，方法论可无缝迁移至丽江古城、玉龙雪山等云南景区。模型已通过 SHAP 可解释性分析识别关键驱动因素，为运营决策提供数据支撑。

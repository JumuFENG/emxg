# 东方财富股票查询库 (EMXG)

一个用于查询东方财富网股票数据并返回DataFrame格式的Python库。

## 功能特性

- 🚀 简单易用的API接口
- 📊 返回pandas DataFrame格式数据
- 🔍 支持多种股票查询方式
- 💾 支持数据导出为CSV/Excel格式
- 🛡️ 自动处理会话和认证
- 📝 完整的日志记录功能
- ⚡ 客户端实例缓存，提高性能
- 🔄 自动数据类型转换和单位处理

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 基本用法

```python
from emxg import EMStockClient, search_emxg

# 方法1: 使用客户端类
client = EMStockClient()

# 获取涨停板股票数据（自动获取所有数据）
df = client.search(keyword="今日涨停", page_size=50)
print(df.head())

# 限制获取数量
df = client.search(keyword="今日涨停", max_count=20)
print(df.head())

# 搜索特定关键词
df = client.search(keyword="涨停板首板", page_size=30, max_page=2)
print(df.head())

# 方法2: 使用便捷函数（推荐）
df = search_emxg("今日涨停", max_count=50)
print(df.head())

# 保存数据
df.to_csv('stocks.csv', index=False, encoding='utf-8-sig')
```

### 运行示例

```bash
# 基本示例
python example.py

# 高级示例（包含数据分析）
python advanced_example.py
```

## API文档

### EMStockClient

主要的客户端类，用于查询股票数据。

#### 方法

- `search(keyword="今日涨停", page_size=50, max_count=None, max_page=None)` - 搜索股票数据

### search_emxg (便捷函数)

推荐使用的便捷函数，内部使用缓存的客户端实例，提高性能。

#### 方法签名

```python
search_emxg(keyword: str, max_count: Optional[int] = None, max_page: Optional[int] = None) -> pd.DataFrame
```

#### 参数说明

- `keyword` - 查询关键词，默认"今日涨停"
- `page_size` - 每页数量，默认50
- `max_count` - 最大返回数据条数，None表示不限制
- `max_page` - 最大页数，None表示不限制

#### 数据自动处理

- **自动分页**: 默认获取所有数据，支持限制条数或页数
- **数值转换**: 自动将"3.42亿"、"7668.05万"等转换为对应数值
- **百分比转换**: 自动将百分比字段转换为小数（如20.05% → 0.2005）
- **数据类型**: 根据API返回的字段信息自动转换数据类型

#### 返回数据字段

返回的DataFrame包含以下主要字段：

- `代码` - 股票代码
- `名称` - 股票名称  
- `最新价` - 最新价格（数值）
- `涨跌幅` - 涨跌幅（小数，如0.2005表示20.05%）
- `成交额` - 成交金额（数值，单位：元）
- `成交量(股)` - 成交量（数值）
- `换手率` - 换手率（小数，如0.1224表示12.24%）
- `市盈率(动)(倍)` - 动态市盈率（数值）
- `市净率(倍)` - 市净率（数值）
- `总市值(日线不复权)` - 总市值（数值，单位：元）
- `流通市值(日线不复权)` - 流通市值（数值，单位：元）

## 使用示例

### 日志配置

库使用标准的Python logging模块，可以通过配置来控制日志输出：

```python
import logging
from emxg import search_emxg

# 配置日志级别和格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 现在可以看到详细的获取过程
df = search_emxg("今日涨停", max_count=20)
```

### 数据分析示例

```python
from emxg import search_emxg

# 使用便捷函数获取数据
df = search_emxg("今日涨停", max_count=50)

# 数据分析（注意：百分比字段已转换为小数）
high_turnover = df[df['换手率'] > 0.10]  # 换手率>10%
print(f"换手率超过10%的股票: {len(high_turnover)}只")

# 按涨跌幅排序
df_sorted = df.sort_values('涨跌幅', ascending=False)
print("涨幅最高的前5只股票:")
for _, row in df_sorted[['名称', '涨跌幅']].head().iterrows():
    print(f"{row['名称']}: {row['涨跌幅']*100:.2f}%")

# 成交额分析（已转换为数值）
high_volume = df[df['成交额'] > 500000000]  # 成交额>5亿
print(f"成交额超过5亿的股票: {len(high_volume)}只")

# 综合筛选：高涨幅 + 高成交额 + 适中换手率
quality_stocks = df[
    (df['涨跌幅'] > 0.15) &  # 涨幅>15%
    (df['成交额'] > 200000000) &  # 成交额>2亿
    (df['换手率'] > 0.05) &  # 换手率>5%
    (df['换手率'] < 0.30)   # 换手率<30%
]
print(f"高质量股票: {len(quality_stocks)}只")
```

## API接口信息

POST: https://np-tjxg-b.eastmoney.com/api/smart-tag/stock/v3/pw/search-code

### 请求参数
- keyWord: 查询关键词，如"今日涨停板首板;"
- pageSize: 每页数量，默认50
- pageNo: 页码，默认1
- fingerprint: 来自cookie中的qgqp_b_id
- timestamp: 微秒时间戳
- requestId: 随机生成的请求ID

>>>>>>> 🎉 Initial release: EMXG v2.0.0

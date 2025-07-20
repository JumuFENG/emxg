# 东财条件选股 (EMXG)

一个用于查询东方财富条件选股数据并返回 DataFrame 格式的 Python 库。

## ⚠️ 重要声明

**EMXG 为开源社区开发，并非东方财富官方提供的工具。** 该工具只是效率工具，为了便于通过 Python 获取东方财富条件选股数据，用于研究和学习，其原理与登录网页获取数据方式一致。

**使用建议：**

- 🔄 **建议低频使用**，反对高频调用
- ⚠️ **高频调用会被东方财富屏蔽**，请自行评估技术和法律风险
- 📖 **项目代码遵循 MIT 开源协议**，但不赞成商用
- ⚖️ **商用请自行评估法律风险**

**感谢东方财富提供免费接口和数据分享。**

## 功能特性

- 🚀 简单易用的 API 接口
- 📊 返回 pandas DataFrame 格式数据
- 🔍 支持多种股票查询方式
- 💾 支持数据导出为 CSV/Excel 格式
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
# 基本示例（快速入门）
python examples/basic_example.py

# 完整示例（包含所有功能演示）
python examples/complete_example.py

# 或使用Makefile
make example              # 运行基本示例
make example-complete     # 运行完整示例
```

## API 文档

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
- `page_size` - 每页数量，默认 50
- `max_count` - 最大返回数据条数，None 表示不限制
- `max_page` - 最大页数，None 表示不限制

#### 数据自动处理

- **自动分页**: 默认获取所有数据，支持限制条数或页数
- **数值转换**: 自动将"3.42 亿"、"7668.05 万"等转换为对应数值
- **百分比转换**: 自动将百分比字段转换为小数（如 20.05% → 0.2005）
- **数据类型**: 根据 API 返回的字段信息自动转换数据类型

#### 返回数据字段

返回的 DataFrame 包含以下主要字段：

- `代码` - 股票代码
- `名称` - 股票名称
- `最新价` - 最新价格（数值）
- `涨跌幅` - 涨跌幅（小数，如 0.2005 表示 20.05%）
- `成交额` - 成交金额（数值，单位：元）
- `成交量(股)` - 成交量（数值）
- `换手率` - 换手率（小数，如 0.1224 表示 12.24%）
- `市盈率(动)(倍)` - 动态市盈率（数值）
- `市净率(倍)` - 市净率（数值）
- `总市值(日线不复权)` - 总市值（数值，单位：元）
- `流通市值(日线不复权)` - 流通市值（数值，单位：元）

## 使用示例

### 日志配置

库使用标准的 Python logging 模块，可以通过配置来控制日志输出：

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

## 命令行工具

EMXG 还提供了便捷的命令行工具：

```bash
# 基本用法
emxg "今日涨停" --max-count 10

# 保存到文件
emxg "涨停板首板" --max-count 20 --output stocks.csv

# 显示详细日志
emxg "连续上涨3天" --verbose

# 查看帮助
emxg --help
```

## 常见问题

### Q: 如何避免被屏蔽？

A: 建议低频使用，避免高频调用。推荐在查询间隔中加入适当的延时。

### Q: 支持哪些查询关键词？

A: 支持东方财富条件选股的所有关键词，如："今日涨停"、"涨停板首板"、"连续上涨 3 天"、"市盈率小于 20"等。

### Q: 数据格式说明

A:

- 百分比字段（如涨跌幅、换手率）已转换为小数形式
- 中文数字单位（如"3.42 亿"）已转换为对应数值
- 所有数值字段都是可直接计算的数值类型

### Q: 如何处理大量数据？

A: 使用`max_count`参数限制数据量，或使用`max_page`限制页数，避免一次性获取过多数据。

## 技术细节

### API 接口信息

- **接口地址**: https://np-tjxg-b.eastmoney.com/api/smart-tag/stock/v3/pw/search-code
- **请求方式**: POST
- **数据格式**: JSON

### 主要参数

- `keyWord`: 查询关键词
- `pageSize`: 每页数量，默认 50
- `pageNo`: 页码，默认 1
- `fingerprint`: 客户端标识
- `timestamp`: 微秒时间戳
- `requestId`: 随机生成的请求 ID

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

- 感谢东方财富提供免费的数据接口
- 感谢开源社区的贡献和支持

# EMXG 使用示例

这个目录包含了 EMXG 库的使用示例，帮助您快速上手。

## 📁 示例文件

### 🚀 [basic_example.py](basic_example.py)

**快速入门示例** - 适合初学者

- ✅ 最简单的查询用法
- ✅ 数据保存方法
- ✅ 多种查询类型展示
- ⏱️ 运行时间: ~30 秒

```bash
python examples/basic_example.py
```

### 🎯 [complete_example.py](complete_example.py)

**完整功能演示** - 展示所有主要功能

- ✅ 基本使用方法
- ✅ 数据转换功能
- ✅ 高级查询技巧
- ✅ 数据分析示例
- ✅ 数据筛选方法
- ✅ 数据导出功能
- ✅ 错误处理展示
- ⏱️ 运行时间: ~2-3 分钟

```bash
python examples/complete_example.py
```

### 🔐 [fingerprint_example.py](fingerprint_example.py)

**浏览器指纹生成示例** - 展示指纹生成功能

- ✅ 基本指纹生成
- ✅ 自定义选项配置
- ✅ 详细指纹信息展示
- ✅ 指纹数据收集
- ✅ 不同配置对比
- ⏱️ 运行时间: ~10秒

```bash
python examples/fingerprint_example.py
```

## 🎯 选择指南

| 需求         | 推荐示例                | 说明                   |
| ------------ | ----------------------- | ---------------------- |
| 快速入门     | `basic_example.py`      | 5 分钟了解基本用法     |
| 学习所有功能 | `complete_example.py`   | 完整功能演示           |
| 生产环境参考 | `complete_example.py`   | 包含错误处理和最佳实践 |
| 指纹生成     | `fingerprint_example.py` | 浏览器指纹生成功能     |

## 🚀 快速开始

1. **安装依赖**:

   ```bash
   pip install -r requirements.txt
   ```

2. **运行基础示例**:

   ```bash
   python examples/basic_example.py
   ```

3. **查看完整功能**:
   ```bash
   python examples/complete_example.py
   ```

## 📊 示例输出

### 基础示例输出

```
🚀 EMXG 基础使用示例
========================================

1️⃣ 查询涨停板股票:
✅ 获取到 5 条数据

📊 股票列表:
  1. ST立方 (300344): 20.04%
  2. 成都先导 (688222): 20.02%
  3. 满坤科技 (301132): 20.01%
  4. 上纬新材 (688585): 20.01%
  5. 南京聚隆 (300644): 20.01%

2️⃣ 保存数据:
✅ 数据已保存到 my_stocks.csv

3️⃣ 其他查询:
  📈 涨停板首板: 找到 3 条
  📈 连续上涨3天: 找到 15 条
  📈 今日跌停: 找到 2 条

🎉 基础示例完成！
```

## 🔧 自定义使用

您可以基于这些示例创建自己的查询脚本：

```python
from emxg import search_emxg

# 自定义查询
df = search_emxg("您的查询条件", max_count=20)

# 数据处理
if not df.empty:
    # 您的数据分析代码
    pass
```

## 💡 提示

- 🔍 支持的查询关键词: "今日涨停"、"涨停板首板"、"连续上涨 3 天"等
- 📊 返回的数据已自动转换格式（百分比 → 小数，中文数字 → 数值）
- 💾 支持导出 CSV、Excel 等格式
- 🖥️ 也可以使用命令行工具: `emxg "今日涨停" --max-count 10`

## 🆘 遇到问题？

1. 查看 [项目文档](../README.md)
2. 检查 [常见问题](../README.md#常见问题)
3. 提交 [Issue](https://github.com/JumuFENG/emxg/issues)

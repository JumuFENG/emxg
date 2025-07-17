# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-17

### Added
- 🚀 新增 `search_emxg` 便捷函数，使用客户端缓存提高性能
- 📝 完整的日志记录功能，支持标准Python logging配置
- 🔄 自动分页获取所有数据，支持 `max_count` 和 `max_page` 参数限制
- 💱 智能数据转换：
  - 中文数字单位转换（3.42亿 → 342000000）
  - 百分比转小数转换（20.05% → 0.2005）
  - 根据API字段信息自动识别数据类型
- 🛡️ 重复列名智能处理，保留所有有用数据
- ⚡ 客户端实例缓存（@lru_cache）
- 🖥️ 命令行工具支持
- 📦 完整的类型注解支持

### Changed
- 🔧 API简化：将三个方法（`query_stocks`、`get_limit_up_stocks`、`search_stocks`）合并为一个 `search` 方法
- 📊 默认行为：自动循环请求获取所有数据，除非指定限制
- 🏷️ 智能列名处理：为重复title添加时间后缀区分（如：归属净利润(2024-12-31)）

### Fixed
- 🐛 修复重复列名导致的数据类型错误
- 🔧 修复 `pd.to_numeric` 参数类型错误
- 🛠️ 改进错误处理和异常信息

### Technical
- 📋 添加完整的 `pyproject.toml` 配置
- 🧪 完善的测试套件
- 📚 更新文档和使用示例
- 🔍 代码质量工具配置（black, isort, mypy, flake8）

## [1.0.0] - 2025-07-17

### Added
- 🎉 初始版本发布
- 📊 基本的股票数据查询功能
- 🐼 返回pandas DataFrame格式数据
- 💾 支持CSV数据导出
- 🔍 支持多种查询关键词

### Features
- `EMStockClient` 主要客户端类
- `query_stocks` 通用查询方法
- `get_limit_up_stocks` 涨停板股票查询
- `search_stocks` 关键词搜索
- 基本的数据处理和转换

---

## 版本说明

### 主要版本 (Major)
- 包含不兼容的API变更
- 重大功能重构

### 次要版本 (Minor)  
- 新增功能，向后兼容
- 性能改进

### 补丁版本 (Patch)
- Bug修复
- 小的改进

---

## 贡献指南

欢迎提交Issue和Pull Request！

### 发布新版本
1. 更新版本号在 `emxg/__init__.py` 和 `pyproject.toml`
2. 更新 `CHANGELOG.md`
3. 创建Git标签：`git tag v2.0.0`
4. 推送标签：`git push origin v2.0.0`
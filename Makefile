# EMXG 项目 Makefile

.PHONY: help install install-dev test test-cov lint format clean build upload docs

# 默认目标
help:
	@echo "EMXG 项目管理命令:"
	@echo ""
	@echo "安装相关:"
	@echo "  install      - 安装项目依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo ""
	@echo "测试相关:"
	@echo "  test         - 运行测试"
	@echo "  test-cov     - 运行测试并生成覆盖率报告"
	@echo ""
	@echo "代码质量:"
	@echo "  lint         - 代码检查"
	@echo "  format       - 代码格式化"
	@echo ""
	@echo "构建发布:"
	@echo "  clean        - 清理构建文件"
	@echo "  build        - 构建包"
	@echo "  upload       - 上传到PyPI"
	@echo ""
	@echo "文档:"
	@echo "  docs         - 生成文档"

# 安装项目依赖
install:
	pip install -e .

# 安装开发依赖
install-dev:
	pip install -e ".[dev]"

# 运行测试
test:
	python -m pytest tests/ -v

# 运行测试并生成覆盖率报告
test-cov:
	python -m pytest tests/ --cov=emxg --cov-report=html --cov-report=term

# 代码检查
lint:
	python -m flake8 emxg/
	python -m mypy emxg/

# 代码格式化
format:
	python -m black emxg/ tests/
	python -m isort emxg/ tests/

# 清理构建文件
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 构建包
build: clean
	python -m build

# 上传到PyPI (需要先配置认证)
upload: build
	python -m twine upload dist/*

# 上传到测试PyPI
upload-test: build
	python -m twine upload --repository testpypi dist/*

# 生成文档 (如果有的话)
docs:
	@echo "文档生成功能待实现"

# 运行基础示例
example:
	python examples/basic_example.py

# 运行完整示例
example-complete:
	python examples/complete_example.py

# 运行所有示例
examples:
	@echo "运行所有示例:"
	@echo "1. 基础示例:"
	python examples/basic_example.py
	@echo "\n2. 完整示例:"
	python examples/complete_example.py

# 检查项目状态
status:
	@echo "项目状态检查:"
	@echo "=============="
	@python -c "import emxg; print(f'版本: {emxg.__version__}')"
	@echo "依赖检查:"
	@python -c "import requests, pandas; print('✓ 核心依赖正常')"
	@echo "功能测试:"
	@python -c "from emxg import search_emxg; print('✓ 导入功能正常')"

# 快速开发测试
dev-test:
	python debug_bug.py
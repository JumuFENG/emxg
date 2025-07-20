"""
测试EMStockClient类
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch

from emxg import EMStockClient, search_emxg


class TestEMStockClient:
    """测试EMStockClient类"""
    
    def test_client_initialization(self):
        """测试客户端初始化"""
        client = EMStockClient()
        assert client.base_url == "https://np-tjxg-b.eastmoney.com/api/smart-tag/stock/v3/pw/search-code"
        assert client.fingerprint is not None
        # fingerprint现在是32位的MD5哈希值
        assert len(client.fingerprint) == 32
    
    def test_generate_request_id(self):
        """测试请求ID生成"""
        client = EMStockClient()
        request_id = client._generate_request_id()
        assert isinstance(request_id, str)
        assert len(request_id) > 32  # 至少32位字符 + 时间戳
    
    def test_convert_chinese_number(self):
        """测试中文数字转换"""
        client = EMStockClient()
        
        # 测试亿单位
        assert client._convert_chinese_number("3.42亿") == 342000000
        assert client._convert_chinese_number("1亿") == 100000000
        
        # 测试万单位
        assert client._convert_chinese_number("7668.05万") == 76680500
        assert client._convert_chinese_number("1万") == 10000
        
        # 测试纯数字
        assert client._convert_chinese_number("123.45") == 123.45
        
        # 测试非字符串
        assert client._convert_chinese_number(123) == 123
        
        # 测试无效字符串
        assert client._convert_chinese_number("无效") == "无效"
    
    def test_convert_percentage(self):
        """测试百分比转换"""
        client = EMStockClient()
        
        # 测试字符串百分比
        assert client._convert_percentage("20.05") == 0.2005
        assert client._convert_percentage("10.5") == 0.105
        assert client._convert_percentage("0") == 0.0
        
        # 测试带%符号
        assert client._convert_percentage("20.05%") == 0.2005
        
        # 测试数字
        assert client._convert_percentage(20.05) == 0.2005
        
        # 测试无效值
        assert client._convert_percentage("无效") == "无效"


class TestSearchEMXG:
    """测试search_emxg便捷函数"""
    
    @patch('emxg.client.EMStockClient')
    def test_search_emxg_basic(self, mock_client_class):
        """测试基本搜索功能"""
        # 模拟客户端和返回数据
        mock_client = Mock()
        mock_df = pd.DataFrame({
            '代码': ['000001', '000002'],
            '名称': ['平安银行', '万科A'],
            '最新价': [10.0, 20.0]
        })
        mock_client.search.return_value = mock_df
        mock_client_class.return_value = mock_client
        
        # 测试搜索
        result = search_emxg("测试关键词", max_count=10)
        
        # 验证结果
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert '代码' in result.columns
        
        # 验证调用参数
        mock_client.search.assert_called_once_with(
            "测试关键词", 
            page_size=50, 
            max_count=10, 
            max_page=None
        )


class TestDataProcessing:
    """测试数据处理功能"""
    
    def test_process_dataframe_with_duplicates(self):
        """测试数据处理功能"""
        client = EMStockClient()
        
        # 模拟columns信息
        columns = [
            {"key": "PARENT_NETPROFIT{2024-12-31}", "title": "归属净利润", "dataType": "Double", "unit": "元"},
            {"key": "PARENT_NETPROFIT{2024-09-30}", "title": "归属净利润", "dataType": "Double", "unit": "元"},
            {"key": "CHG", "title": "涨跌幅", "dataType": "Double", "unit": "%"}
        ]
        
        # 模拟DataFrame（使用原始key作为列名）
        df = pd.DataFrame({
            "PARENT_NETPROFIT{2024-12-31}": [1000000, 2000000],
            "PARENT_NETPROFIT{2024-09-30}": [800000, 1800000],
            "CHG": [10.5, 8.2]
        })
        
        # 测试_process_dataframe方法（只处理数据转换，不处理列名）
        result = client._process_dataframe(df, columns)
        
        # 验证数据转换（列名保持原样）
        assert "PARENT_NETPROFIT{2024-12-31}" in result.columns
        assert "PARENT_NETPROFIT{2024-09-30}" in result.columns
        assert "CHG" in result.columns
        
        # 验证百分比转换
        assert result["CHG"].iloc[0] == 0.105  # 10.5% -> 0.105
        assert result["CHG"].iloc[1] == 0.082  # 8.2% -> 0.082


if __name__ == "__main__":
    pytest.main([__file__])
"""
东方财富条件选股
查询并返回DataFrame格式
"""

from .client import EMStockClient, search_emxg

__version__ = "2.0.0"
__all__ = ["EMStockClient", "search_emxg"]
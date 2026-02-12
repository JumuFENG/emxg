"""
东方财富条件选股
查询并返回DataFrame格式
"""

from .client import EMStockClient, search_emxg
from .data_adapter import DataFrame
from .emfinger import get_printfinger
from .wencai_client import WencaiStockClient, search_wencai


__version__ = "2.2.6"


def search(keyword: str, max_count: int = None, max_page: int = None) -> DataFrame:
    result = search_wencai(keyword, max_count=max_count, max_page=max_page)
    if result is not None:
        return result
    return search_emxg(keyword, max_count=max_count, max_page=max_page)


__all__ = ["EMStockClient", "search_emxg", "get_printfinger", "DataFrame", "add_column", "WencaiStockClient", "search_wencai", "search"]

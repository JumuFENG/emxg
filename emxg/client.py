"""
东方财富条件选股查询
"""

import logging
import string
import random
import time
import requests
from typing import Optional, Union, List, Dict, Any
from functools import lru_cache

from .data_adapter import DataProcessor, DataFrame
from .emfinger import get_printfinger


logger = logging.getLogger(__package__)


class EMStockClient:
    """东方财富条件选股查询客户端 - 适配器版本"""

    def __init__(self):
        self.base_url = "https://np-tjxg-b.eastmoney.com/api/smart-tag/stock/v3/pw/search-code"
        self.session = requests.Session()
        self.data_processor = DataProcessor()
        self.fingerprint = get_printfinger()

    def _generate_request_id(self, length: int = 32) -> str:
        """生成请求ID"""
        chars = string.ascii_letters + string.digits
        rand_str = ''.join(random.choices(chars, k=length))
        timestamp = str(int(time.time() * 1000000))  # 微秒时间戳
        return rand_str + timestamp

    def search(self,
               keyword: str = "今日涨停",
               page_size: int = 50,
               max_count: Optional[int] = None,
               max_page: Optional[int] = None) -> Union[DataFrame, List[Dict[str, Any]]]:
        """
        搜索股票数据

        Args:
            keyword: 查询关键词，默认为"今日涨停"
            page_size: 每页数量，默认50
            max_count: 最大返回数据条数，None表示不限制
            max_page: 最大页数，None表示不限制

        Returns:
            Union[DataFrame, List[Dict]]: 股票数据，有pandas返回DataFrame，否则返回字典列表
        """
        all_data = []
        page_no = 1
        xc_id = ""  # 首次请求为空

        while True:
            # 构建请求数据
            request_data = {
                "keyWord": keyword,
                "pageSize": page_size,
                "pageNo": page_no,
                "fingerprint": self.fingerprint,
                "gids": [],
                "matchWord": "",
                "timestamp": str(int(time.time() * 1000000)),
                "shareToGuba": False,
                "requestId": self._generate_request_id(),
                "needCorrect": True,
                "removedConditionIdList": [],
                "xcId": xc_id,
                "ownSelectAll": False,
                "dxInfo": [],
                "extraCondition": ""
            }

            try:
                response = self.session.post(
                    self.base_url,
                    json=request_data,
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()

                if data.get("code") != "100":
                    if page_no == 1:  # 第一页就失败，抛出异常
                        raise Exception(f"API返回错误: {data.get('msg', '未知错误')}")
                    else:  # 后续页面失败，可能是没有更多数据了
                        break

                # 解析数据
                result = data.get("data", {}).get("result", {})
                columns = result.get("columns", [])
                data_list = result.get("dataList", [])
                total = result.get("total", 0)

                # 更新xcId用于下次请求
                if "xcId" in result:
                    xc_id = result["xcId"]

                if not data_list:
                    break

                # 添加当前页数据
                all_data.extend(data_list)

                logger.debug(f"已获取第{page_no}页数据，本页{len(data_list)}条，累计{len(all_data)}条")

                # 检查是否达到限制条件
                if max_count and len(all_data) >= max_count:
                    all_data = all_data[:max_count]
                    break

                if max_page and page_no >= max_page:
                    break

                # 检查是否还有更多数据
                if len(data_list) < page_size or len(all_data) >= total:
                    break

                page_no += 1

            except Exception as e:
                if page_no == 1:
                    raise Exception(f"查询失败: {str(e)}")
                else:
                    logger.warning(f"第{page_no}页处理失败，停止获取: {str(e)}")
                    break

        if not all_data:
            return DataFrame([])

        # 使用适配器处理数据
        df = self.data_processor.process_data(all_data, columns)

        logger.info(f"查询完成，共获取{len(df)}条数据")

        # 根据环境返回不同的数据类型
        return df


# 缓存的客户端实例
@lru_cache(maxsize=1)
def create_client() -> EMStockClient:
    """创建并缓存EMStockClient实例"""
    return EMStockClient()


def search_emxg(keyword: str, max_count: Optional[int] = None,
               max_page: Optional[int] = None) -> Union[DataFrame, List[Dict[str, Any]]]:
    """
    便捷的股票搜索函数，使用缓存的客户端实例

    Args:
        keyword: 查询关键词
        max_count: 最大返回数据条数，None表示不限制
        max_page: 最大页数，None表示不限制

    Returns:
        Union[DataFrame, List[Dict]]: 股票数据，有pandas返回DataFrame，否则返回字典列表
    """
    client = create_client()
    return client.search(keyword, page_size=50, max_count=max_count, max_page=max_page)


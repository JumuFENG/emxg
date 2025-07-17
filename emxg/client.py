"""
东方财富条件选股查询
"""

import logging
import requests
import pandas as pd
import string
import random
import time
import re
from typing import Optional, Union
from functools import lru_cache

logger = logging.getLogger('emxg')

class EMStockClient:
    """东方财富条件选股查询
    entry_url = "https://xuangu.eastmoney.com/"
    fingerprint = "4f7ce80cd5a83922d38c2a231af461ed"
    """
    
    def __init__(self):
        self.base_url = "https://np-tjxg-b.eastmoney.com/api/smart-tag/stock/v3/pw/search-code"
        self.session = requests.Session()
        self.fingerprint = self._simple_fingerprint()
    
    def _simple_fingerprint(self):
        f = f'{random.randint(1, 9)}'
        for i in range(19):
            f += str(random.randint(0, 8))
        return f

    def _generate_request_id(self, length: int = 32) -> str:
        """生成请求ID"""
        chars = string.ascii_letters + string.digits
        rand_str = ''.join(random.choices(chars, k=length))
        timestamp = str(int(time.time() * 1000000))  # 微秒时间戳
        return rand_str + timestamp
    
    def _convert_chinese_number(self, value: str) -> float:
        """
        转换中文数字单位为数值
        例: "3.42亿" -> 342000000, "7668.05万" -> 76680500
        """
        if not isinstance(value, str):
            return value
        
        # 移除空格
        value = value.strip()
        
        # 如果是纯数字，直接返回
        try:
            return float(value)
        except ValueError:
            pass
        
        # 处理带单位的数字
        if '亿' in value:
            number_part = value.replace('亿', '')
            try:
                return float(number_part) * 100000000  # 1亿 = 100,000,000
            except ValueError:
                return value
        elif '万' in value:
            number_part = value.replace('万', '')
            try:
                return float(number_part) * 10000  # 1万 = 10,000
            except ValueError:
                return value
        
        return value
    
    def _convert_percentage(self, value: str) -> float:
        """
        转换百分比为小数
        例: "20.05" -> 0.2005, "10.5" -> 0.105
        """
        if not isinstance(value, str):
            try:
                return round(float(value) / 100, 4)
            except (ValueError, TypeError):
                return value
        
        try:
            # 移除可能的%符号
            clean_value = value.replace('%', '').strip()
            return round(float(clean_value) / 100, 4)
        except (ValueError, TypeError):
            return value
    
    def _process_dataframe(self, df: pd.DataFrame, columns_info: list) -> pd.DataFrame:
        """
        处理DataFrame，根据columns信息转换数值字段
        
        Args:
            df: 原始DataFrame
            columns_info: API返回的columns信息
            
        Returns:
            处理后的DataFrame
        """
        if df.empty:
            return df
        
        df_processed = df.copy()
        
        # 根据columns信息确定需要转换的字段
        for col_info in columns_info:
            key = col_info.get("key", "")
            title = col_info.get("title", key)
            data_type = col_info.get("dataType", "")
            unit = col_info.get("unit", "")
            
            # 确定要处理的列名（优先使用中文列名）
            col_name = title if title in df_processed.columns else key
            
            if col_name not in df_processed.columns:
                continue
            
            # 根据dataType和unit进行相应的转换
            if data_type in ["Double", "Long", "Integer"]:
                try:
                    # 数值类型，先尝试中文数字转换
                    df_processed[col_name] = df_processed[col_name].apply(self._convert_chinese_number)
                    
                    # 如果单位是%，转换为小数
                    if unit == "%":
                        df_processed[col_name] = df_processed[col_name].apply(self._convert_percentage)
                    else:
                        # 确保传递给pd.to_numeric的是Series对象
                        if isinstance(df_processed[col_name], pd.Series):
                            df_processed[col_name] = pd.to_numeric(df_processed[col_name], errors='coerce')
                        else:
                            logger.warning(f"列 {col_name} 不是Series类型，跳过数值转换")
                except Exception as e:
                    logger.warning(f"处理列 {col_name} 时出错: {e}")
                    continue
            elif data_type == "Boolean":
                # 布尔类型转换
                df_processed[col_name] = df_processed[col_name].apply(
                    lambda x: True if str(x).strip() in ['首板', 'True', '1', 'true'] else False
                )
        
        return df_processed
    
    def search(self, 
               keyword: str = "今日涨停",
               page_size: int = 50,
               max_count: Optional[int] = None,
               max_page: Optional[int] = None) -> pd.DataFrame:
        """
        搜索股票数据
        
        Args:
            keyword: 查询关键词，默认为"今日涨停"
            page_size: 每页数量，默认50
            max_count: 最大返回数据条数，None表示不限制
            max_page: 最大页数，None表示不限制
            
        Returns:
            pandas.DataFrame: 股票数据
        """
        all_data = []
        page_no = 1
        xc_id = ""  # 首次请求为空
        total_count = 0
        
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
                response = self.session.post(self.base_url, json=request_data)
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
                
                logger.info(f"已获取第{page_no}页数据，本页{len(data_list)}条，累计{len(all_data)}条")
                
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
                
            except requests.RequestException as e:
                if page_no == 1:
                    raise Exception(f"网络请求失败: {str(e)}")
                else:
                    logger.warning(f"第{page_no}页请求失败，停止获取: {str(e)}")
                    break
            except Exception as e:
                if page_no == 1:
                    raise Exception(f"查询失败: {str(e)}")
                else:
                    logger.warning(f"第{page_no}页处理失败，停止获取: {str(e)}")
                    break
        
        if not all_data:
            return pd.DataFrame()
        
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        # 处理数据转换
        if columns:
            # 1. 首先检查并处理重复的key
            original_keys = [col.get("key", "") for col in columns]
            duplicate_keys = [key for key in original_keys if original_keys.count(key) > 1 and key != ""]
            
            if duplicate_keys:
                logger.warning(f"检测到重复的key: {list(set(duplicate_keys))}")
                # 只保留第一个出现的key
                seen_keys = set()
                columns_filtered = []
                for col in columns:
                    key = col.get("key", "")
                    if key == "" or key not in seen_keys:
                        columns_filtered.append(col)
                        if key != "":
                            seen_keys.add(key)
                
                columns = columns_filtered
                logger.info(f"去重后保留列定义数: {len(columns)}")
            
            # 2. 处理列名映射，为重复的title添加区分后缀
            column_mapping = {}
            title_counts = {}
            
            for col in columns:
                key = col.get("key", "")
                title = col.get("title", key)
                
                if key and key in df.columns:
                    # 如果title重复，添加后缀区分
                    if title in title_counts:
                        title_counts[title] += 1
                        # 从key中提取时间信息作为后缀
                        if '{' in key and '}' in key:
                            time_part = key[key.find('{')+1:key.find('}')]
                            unique_title = f"{title}({time_part})"
                        else:
                            unique_title = f"{title}_{title_counts[title]}"
                    else:
                        title_counts[title] = 1
                        unique_title = title
                    
                    column_mapping[key] = unique_title
            
            # 3. 重命名列
            df = df.rename(columns=column_mapping)
            
            # 4. 处理数值转换
            df = self._process_dataframe(df, columns)
        
        logger.info(f"查询完成，共获取{len(df)}条数据")
        return df

@lru_cache(maxsize=1)
def create_client() -> EMStockClient:
    """创建并缓存EMStockClient实例"""
    return EMStockClient()

def search_emxg(keyword: str, max_count: Optional[int] = None, max_page: Optional[int] = None) -> pd.DataFrame:
    """
    便捷的股票搜索函数，使用缓存的客户端实例
    
    Args:
        keyword: 查询关键词
        max_count: 最大返回数据条数，None表示不限制
        max_page: 最大页数，None表示不限制
        
    Returns:
        pandas.DataFrame: 股票数据
    """
    client = create_client()
    return client.search(keyword, page_size=50, max_count=max_count, max_page=max_page)

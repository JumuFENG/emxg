"""
数据处理适配器模块
自动选择 pandas 或纯Python实现数据处理功能
"""

import logging
from typing import Any, Dict, List, Optional, Union, Tuple
import importlib.util

logger = logging.getLogger(__package__)


if importlib.util.find_spec("pandas") is None:
    import csv

    class DataFrame:
        """DataFrame适配器类"""

        def __init__(self, data: List[Dict[str, Any]],
                    columns: Optional[List[Dict[str, Any]]] = None):
            self.data = data.copy() if data else []

        @property
        def empty(self) -> bool:
            """检查数据是否为空"""
            return len(self.data) == 0

        @property
        def columns(self) -> List[str]:
            """获取列名列表"""
            return list(self.data[0].keys()) if self.data else []

        @property
        def shape(self) -> Tuple[int, int]:
            """获取数据形状"""
            return (len(self.data), len(self.columns) if self.data else 0)

        def head(self, n: int = 5) -> 'DataFrame':
            """获取前n行数据"""
            return DataFrame(data=self.data[:n])

        def filter(self, condition) -> 'DataFrame':
            """根据条件过滤数据"""
            filtered_data = []
            for row in self.data:
                if condition(row):
                    filtered_data.append(row)
            return DataFrame(data=filtered_data)

        def sort_values(self, by: str, ascending: bool = True) -> 'DataFrame':
            """按指定列排序"""
            if not self.data or by not in self.columns:
                return self

            sorted_data = sorted(self.data, key=lambda x: x.get(by, 0), reverse=not ascending)
            return DataFrame(data=sorted_data)

        def to_csv(self, filepath: str, index: bool = False, encoding: str = 'utf-8') -> None:
            """保存为CSV文件"""
            if not self.data:
                return

            fieldnames = self.columns
            with open(filepath, 'w', newline='', encoding=encoding) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not index:
                    writer.writeheader()
                writer.writerows(self.data)

        def to_excel(self, filepath: str, index: bool = False) -> None:
            """保存为Excel文件（需要openpyxl库）"""
            if not self.data:
                return
            try:
                from openpyxl import Workbook
            except ImportError:
                raise ImportError("请安装 openpyxl 库以支持 Excel 导出: pip install openpyxl")

            wb = Workbook()
            ws = wb.active
            if not index:
                ws.append(self.columns)
            for row in self.data:
                ws.append([row.get(col, '') for col in self.columns])
            wb.save(filepath)

        def to_dict(self, orient: str = 'records') -> Union[List[Dict], Dict]:
            """转换为字典格式"""
            if orient == 'records':
                return self.data
            elif orient == 'dict':
                result = {}
                for col in self.columns:
                    result[col] = [row.get(col) for row in self.data]
                return result
            else:
                raise ValueError(f"不支持的orient参数: {orient}")

        def __len__(self) -> int:
            """返回数据行数"""
            return len(self.data)

        def __getitem__(self, key):
            """支持列访问"""
            if isinstance(key, str):
                return [row.get(key) for row in self.data]
            elif isinstance(key, slice):
                return DataFrame(data=self.data[key])
            else:
                raise KeyError(f"不支持的key类型: {type(key)}")

        def __iter__(self):
            """支持迭代"""
            return enumerate(self.data)

        def rename(self, columns: Dict[str, str]) -> 'DataFrame':
            """重命名列"""
            for row in self.data:
                for old_key, new_key in columns.items():
                    if old_key in row:
                        row[new_key] = row.pop(old_key)
            return self

    def process_column_mapping(df: DataFrame, columns_info: List[Dict[str, Any]]) -> DataFrame:
        """使用纯Python处理列名映射"""
        # 处理列名映射
        column_mapping = {}
        title_counts = {}

        for col in columns_info:
            key = col.get("key", "")
            title = col.get("title", key) if 'title' in col else col.get('index_name', key)

            if key and key in df.columns and df.data[0] and key in df.data[0]:
                if title in title_counts:
                    title_counts[title] += 1
                    if '{' in key and '}' in key:
                        time_part = key[key.find('{')+1:key.find('}')]
                        unique_title = f"{title}({time_part})"
                    else:
                        unique_title = f"{title}_{title_counts[title]}"
                else:
                    title_counts[title] = 1
                    unique_title = title

                column_mapping[key] = unique_title

        df.rename(column_mapping)
        return df

    def convert_column(df: DataFrame, column_name: str, converter) -> None:
        """转换指定列的数据"""
        for row in df.data:
            if column_name in row:
                row[column_name] = converter(row[column_name])
        return df

    def concat(dfs: List[DataFrame], ignore_index=True) -> DataFrame:
        """连接多个DataFrame"""
        combined_data = []
        for df in dfs:
            combined_data.extend(df.data)
        return DataFrame(data=combined_data)

else:
    import pandas as pd
    DataFrame = pd.DataFrame

    def process_column_mapping(df: DataFrame, columns_info: List[Dict[str, Any]]) -> DataFrame:
        """使用pandas处理列名映射"""
        # 处理列名映射
        column_mapping = {}
        title_counts = {}

        for col in columns_info:
            key = col.get("key", "")
            title = col.get("title", key) if 'title' in col else col.get('index_name', key)

            if key and key in df.columns:
                if title in title_counts:
                    title_counts[title] += 1
                    if '{' in key and '}' in key:
                        time_part = key[key.find('{')+1:key.find('}')]
                        unique_title = f"{title}({time_part})"
                    else:
                        unique_title = f"{title}_{title_counts[title]}"
                else:
                    title_counts[title] = 1
                    unique_title = title

                column_mapping[key] = unique_title

        # 重命名列
        df = df.rename(columns=column_mapping)
        return df

    def convert_column(df: DataFrame, column_name: str, converter) -> None:
        """转换指定列的数据"""
        df[column_name] = df[column_name].apply(converter)
        return df

    def concat(dfs: List[DataFrame], ignore_index=True) -> DataFrame:
        """连接多个DataFrame"""
        return pd.concat(dfs, ignore_index=True)

class DataProcessor:
    """数据处理适配器类"""

    def create_dataframe(self, data: List[Dict[str, Any]],
                      columns: Optional[List[Dict[str, Any]]] = None) -> 'DataFrame':
        """
        创建数据结构

        Args:
            data: 原始数据列表
            columns: 列信息定义

        Returns:
            DataFrame适配器对象
        """
        return DataFrame(data=data, columns=columns)

    def process_data(self, data: List[Dict[str, Any]],
                   columns_info: List[Dict[str, Any]]) -> 'DataFrame':
        """
        处理原始数据，包括类型转换和数据处理

        Args:
            data: 原始数据列表
            columns_info: 列信息定义

        Returns:
            处理后的DataFrame适配器对象
        """
        # 首先创建DataFrame
        df = self.create_dataframe(data)

        # 处理列名映射和数据转换
        if columns_info:
            df = self._process_column_mapping(df, columns_info)
            df = self._convert_data_types(df, columns_info)

        return df

    def _process_column_mapping(self, df: 'DataFrame',
                            columns_info: List[Dict[str, Any]]) -> 'DataFrame':
        """处理列名映射"""
        original_keys = [col.get("key", "") for col in columns_info]
        duplicate_keys = [key for key in original_keys if original_keys.count(key) > 1 and key != ""]

        if duplicate_keys:
            logger.warning(f"检测到重复的key: {list(set(duplicate_keys))}")
            # 只保留第一个出现的key
            seen_keys = set()
            columns_filtered = []
            for col in columns_info:
                key = col.get("key", "")
                if key == "" or key not in seen_keys:
                    columns_filtered.append(col)
                    if key != "":
                        seen_keys.add(key)
            columns_info = columns_filtered
            logger.info(f"去重后保留列定义数: {len(columns_info)}")

        return process_column_mapping(df, columns_info)

    def _convert_data_types(self, df: 'DataFrame',
                         columns_info: List[Dict[str, Any]]) -> 'DataFrame':
        """转换数据类型"""
        for col_info in columns_info:
            key = col_info.get("key", "")
            title = col_info.get("title", key) if 'title' in col_info else col_info.get('index_name', key)
            data_type = col_info.get("dataType", "") if 'dataType' in col_info else col_info.get('type', '')
            if data_type is None:
                data_type = ""
            unit = col_info.get("unit", "")

            # 确定要处理的列名
            col_name = title if title in df.columns else key
            if not col_name in df.columns:
                continue

            if data_type.upper() in ["DOUBLE", "LONG", "INTEGER"]:
                df = convert_column(df, col_name, self._convert_chinese_number)

                # 如果单位是%，转换为小数
                if unit == "%":
                    df = convert_column(df, col_name, self._convert_percentage)

            elif data_type.upper() == "BOOLEAN":
                # 布尔类型转换
                df = convert_column(df, col_name, lambda x: str(x).strip() in ['首板', 'True', '1', 'true'])

        return df

    def _convert_chinese_number(self, value: Any) -> Union[float, str]:
        """转换中文数字单位为数值"""
        if not isinstance(value, str):
            return value

        value = value.strip()

        try:
            return float(value)
        except ValueError:
            pass

        if '亿' in value:
            number_part = value.replace('亿', '')
            try:
                return float(number_part) * 100000000
            except ValueError:
                return value
        elif '万' in value:
            number_part = value.replace('万', '')
            try:
                return float(number_part) * 10000
            except ValueError:
                return value

        return value

    def _convert_percentage(self, value: Any) -> Union[float, Any]:
        """转换百分比为小数"""
        if not isinstance(value, str):
            try:
                return round(float(value) / 100, 4)
            except (ValueError, TypeError):
                return value

        try:
            clean_value = value.replace('%', '').strip()
            return round(float(clean_value) / 100, 4)
        except (ValueError, TypeError):
            return value


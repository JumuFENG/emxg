#!/usr/bin/env python3
"""
EMXG 命令行工具
"""

import argparse
import logging
import sys
from typing import Optional

from . import search_emxg, __version__


def setup_logging(verbose: bool = False) -> None:
    """设置日志配置"""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="东方财富股票查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  emxg "今日涨停" --max-count 10
  emxg "涨停板首板" --max-page 2 --output stocks.csv
  emxg "连续4个季度亏损大于1000万" --verbose
        """
    )
    
    parser.add_argument(
        "keyword",
        help="查询关键词，如：今日涨停、涨停板首板等"
    )
    
    parser.add_argument(
        "--max-count",
        type=int,
        help="最大返回数据条数"
    )
    
    parser.add_argument(
        "--max-page",
        type=int,
        help="最大页数"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（CSV格式）"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细日志"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"emxg {__version__}"
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    
    try:
        # 执行查询
        print(f"正在查询: {args.keyword}")
        df = search_emxg(
            keyword=args.keyword,
            max_count=args.max_count,
            max_page=args.max_page
        )
        
        if df.empty:
            print("未找到相关数据")
            sys.exit(1)
        
        print(f"找到 {len(df)} 条数据")
        
        # 显示基本信息
        if '名称' in df.columns and '代码' in df.columns:
            print("\n前10条结果:")
            for i, (_, row) in enumerate(df.head(10).iterrows()):
                name = row.get('名称', 'N/A')
                code = row.get('代码', 'N/A')
                price = row.get('最新价', 'N/A')
                chg = row.get('涨跌幅', 'N/A')
                
                # 格式化显示
                price_str = f"{price}元" if price != 'N/A' else 'N/A'
                chg_str = f"{chg*100:.2f}%" if isinstance(chg, (int, float)) else str(chg)
                
                print(f"  {i+1:2d}. {name} ({code}): {price_str}, {chg_str}")
        
        # 保存文件
        if args.output:
            df.to_csv(args.output, index=False, encoding='utf-8-sig')
            print(f"\n数据已保存到: {args.output}")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"查询失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
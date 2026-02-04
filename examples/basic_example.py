#!/usr/bin/env python3
"""
EMXG 基础使用示例
快速入门东方财富股票查询库
"""

from emxg import search_emxg, search_wencai


def main():
    """基础使用示例"""
    print("🚀 EMXG 基础使用示例")
    print("=" * 40)
    
    # 1. 最简单的用法
    print("\n1️⃣ 查询涨停板股票:")
    df = search_emxg("今日涨停", max_count=5)
    
    if not df.empty:
        print(f"✅ 获取到 {len(df)} 条数据")
        
        # 显示基本信息
        if '名称' in df.columns and '涨跌幅' in df.columns:
            print("\n📊 股票列表:")
            for i, (_, row) in enumerate(df.head().iterrows()):
                name = row.get('名称', 'N/A')
                code = row.get('代码', 'N/A')
                chg = row.get('涨跌幅', 0)
                chg_str = f"{chg*100:.2f}%" if isinstance(chg, (int, float)) else str(chg)
                print(f"  {i+1}. {name} ({code}): {chg_str}")
    
    # 2. 保存数据
    print(f"\n2️⃣ 保存数据:")
    if not df.empty:
        df.to_csv('my_stocks.csv', index=False, encoding='utf-8-sig')
        print("✅ 数据已保存到 my_stocks.csv")
    
    # 3. 其他查询示例
    print(f"\n3️⃣ 其他查询:")
    
    # 查询不同类型的股票
    queries = [
        "涨停板首板",
        "连续上涨3天",
        "今日跌停"
    ]
    
    for query in queries:
        try:
            result = search_emxg(query, max_count=3)
            status = f"找到 {len(result)} 条" if not result.empty else "无数据"
            print(f"  📈 {query}: {status}")
        except Exception as e:
            print(f"  ❌ {query}: 查询失败")
    
    print(f"\n🎉 基础示例完成！")
    print("💡 运行 complete_example.py 查看更多高级功能")


def myquery():
    # query = '昨天阳线 今天阴线 收盘价>ma10且收盘价<(ma5+ma10)/2 最近5天都是小阴小阳线 ma10>ma30'
    query = '今日涨停'
    try:
        result = search_emxg(query)
        status = f"找到 {len(result)} 条" if not result.empty else "无数据"
        print(f"  📈 {query}: {status}")
    except Exception as e:
        print(f"  ❌ {query}: 查询失败")
        print(str(e))

def wencai_query():
    query = '涨幅大于8%'
    try:
        result = search_wencai(query)
        status = f"找到 {len(result)} 条" if not result.empty else "无数据"
        print(f"  📈 {query}: {status}")
    except Exception as e:
        print(f"  ❌ {query}: 查询失败")
        print(str(e))

if __name__ == "__main__":
    wencai_query()
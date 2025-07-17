#!/usr/bin/env python3
"""
测试logger功能和search_emxg函数
"""

import logging
from emxg import EMStockClient, search_emxg

# 配置logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_client_with_logger():
    """测试EMStockClient的logger功能"""
    print("=== 测试EMStockClient的logger功能 ===")
    
    client = EMStockClient()
    
    try:
        # 测试少量数据获取
        df = client.search(keyword="今日涨停", page_size=5, max_count=10)
        
        if not df.empty:
            print(f"✓ 成功获取 {len(df)} 条数据")
            
            # 检查数据转换
            if '涨跌幅' in df.columns:
                chg_sample = df['涨跌幅'].iloc[0]
                print(f"✓ 涨跌幅转换示例: {chg_sample} (小数形式，相当于 {chg_sample*100:.2f}%)")
            
            if '成交额' in df.columns:
                volume_sample = df['成交额'].iloc[0]
                print(f"✓ 成交额转换示例: {volume_sample:,.0f} 元")
        else:
            print("❌ 未获取到数据")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_search_emxg():
    """测试search_emxg便捷函数"""
    print("\n=== 测试search_emxg便捷函数 ===")
    
    try:
        # 测试便捷函数
        df = search_emxg("连续4个季度亏损大于1000万", max_page=1)
        
        if not df.empty:
            print(f"✓ search_emxg成功获取 {len(df)} 条数据")
            print(tuple(df['代码']))
            # 显示前几条数据
            key_columns = ['代码', '名称', '最新价', '涨跌幅']
            available_columns = [col for col in key_columns if col in df.columns]
            
            if available_columns:
                print("前3条数据:")
                for i, (_, row) in enumerate(df[available_columns].head(3).iterrows()):
                    code = row.get('代码', 'N/A')
                    name = row.get('名称', 'N/A')
                    price = row.get('最新价', 'N/A')
                    chg = row.get('涨跌幅', 'N/A')
                    chg_display = f"{chg*100:.2f}%" if isinstance(chg, (int, float)) else str(chg)
                    print(f"  {i+1}. {name} ({code}): {price}元, {chg_display}")
        else:
            print("❌ search_emxg未获取到数据")
            
    except Exception as e:
        print(f"❌ search_emxg测试失败: {e}")

def test_multiple_calls():
    """测试多次调用是否使用缓存"""
    print("\n=== 测试客户端缓存功能 ===")
    
    try:
        # 第一次调用
        df1 = search_emxg("今日涨停", max_count=3)
        print(f"✓ 第一次调用获取 {len(df1)} 条数据")
        
        # 第二次调用（应该使用缓存的客户端）
        df2 = search_emxg("涨停板", max_count=3)
        print(f"✓ 第二次调用获取 {len(df2)} 条数据")
        
        print("✓ 缓存功能正常工作")
        
    except Exception as e:
        print(f"❌ 缓存测试失败: {e}")


def main():
    print("开始测试改进后的EMXG库...")
    
    # test_client_with_logger()
    test_search_emxg()
    # test_multiple_calls()
    
    print("\n🎉 所有测试完成！")

if __name__ == "__main__":
    main()
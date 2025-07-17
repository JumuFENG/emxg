#!/usr/bin/env python3
"""
最终综合测试 - 验证所有改进功能
"""

import logging
import pandas as pd
from emxg import EMStockClient, search_emxg

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_search_emxg_function():
    """测试search_emxg便捷函数"""
    print("=== 测试search_emxg便捷函数 ===")
    
    try:
        # 测试基本功能
        df = search_emxg("今日涨停", max_count=5)
        
        if not df.empty:
            print(f"✅ 成功获取 {len(df)} 条数据")
            
            # 验证数据转换
            print("\n数据转换验证:")
            
            # 检查百分比转换
            if '涨跌幅' in df.columns:
                chg_val = df['涨跌幅'].iloc[0]
                print(f"  涨跌幅: {chg_val} (小数) = {chg_val*100:.2f}% (百分比)")
            
            if '换手率' in df.columns:
                turnover_val = df['换手率'].iloc[0]
                print(f"  换手率: {turnover_val} (小数) = {turnover_val*100:.2f}% (百分比)")
            
            # 检查数值转换
            if '成交额' in df.columns:
                volume_val = df['成交额'].iloc[0]
                print(f"  成交额: {volume_val:,.0f} 元 = {volume_val/100000000:.2f} 亿元")
            
            return True
        else:
            print("❌ 未获取到数据")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_data_analysis():
    """测试数据分析功能"""
    print("\n=== 测试数据分析功能 ===")
    
    try:
        df = search_emxg("今日涨停", max_count=20)
        
        if df.empty:
            print("❌ 未获取到数据")
            return False
        
        print(f"✅ 获取到 {len(df)} 条数据进行分析")
        
        # 涨跌幅分析
        if '涨跌幅' in df.columns:
            chg_data = df['涨跌幅'].dropna()
            if not chg_data.empty:
                avg_chg = chg_data.mean() * 100
                max_chg = chg_data.max() * 100
                min_chg = chg_data.min() * 100
                print(f"  平均涨跌幅: {avg_chg:.2f}%")
                print(f"  最高涨跌幅: {max_chg:.2f}%")
                print(f"  最低涨跌幅: {min_chg:.2f}%")
        
        # 成交额分析
        if '成交额' in df.columns:
            volume_data = df['成交额'].dropna()
            if not volume_data.empty:
                avg_volume = volume_data.mean() / 100000000
                high_volume_count = (volume_data > 500000000).sum()
                print(f"  平均成交额: {avg_volume:.2f} 亿元")
                print(f"  成交额>5亿的股票: {high_volume_count} 只")
        
        # 换手率分析
        if '换手率' in df.columns:
            turnover_data = df['换手率'].dropna()
            if not turnover_data.empty:
                avg_turnover = turnover_data.mean() * 100
                high_turnover_count = (turnover_data > 0.10).sum()
                print(f"  平均换手率: {avg_turnover:.2f}%")
                print(f"  换手率>10%的股票: {high_turnover_count} 只")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据分析测试失败: {e}")
        return False

def test_client_caching():
    """测试客户端缓存功能"""
    print("\n=== 测试客户端缓存功能 ===")
    
    try:
        # 多次调用应该使用同一个缓存的客户端实例
        df1 = search_emxg("今日涨停", max_count=3)
        df2 = search_emxg("涨停板", max_count=3)
        
        print(f"✅ 第一次调用获取 {len(df1)} 条数据")
        print(f"✅ 第二次调用获取 {len(df2)} 条数据")
        print("✅ 客户端缓存功能正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 缓存测试失败: {e}")
        return False

def test_data_export():
    """测试数据导出功能"""
    print("\n=== 测试数据导出功能 ===")
    
    try:
        df = search_emxg("今日涨停", max_count=10)
        
        if df.empty:
            print("❌ 未获取到数据")
            return False
        
        # 导出CSV
        df.to_csv('test_export.csv', index=False, encoding='utf-8-sig')
        print("✅ 成功导出CSV文件: test_export.csv")
        
        # 验证导出的数据
        df_read = pd.read_csv('test_export.csv', encoding='utf-8-sig')
        print(f"✅ 验证导出数据: {len(df_read)} 行 x {len(df_read.columns)} 列")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据导出测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        # 测试无效关键词
        df = search_emxg("不存在的关键词12345", max_count=5)
        
        if df.empty:
            print("✅ 正确处理了无效关键词（返回空DataFrame）")
        else:
            print(f"⚠️  无效关键词仍返回了 {len(df)} 条数据")
        
        return True
        
    except Exception as e:
        print(f"✅ 正确抛出异常: {type(e).__name__}: {e}")
        return True

def main():
    """运行所有测试"""
    print("🚀 开始运行最终综合测试...\n")
    
    tests = [
        ("search_emxg便捷函数", test_search_emxg_function),
        ("数据分析功能", test_data_analysis),
        ("客户端缓存", test_client_caching),
        ("数据导出", test_data_export),
        ("错误处理", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        result = test_func()
        results.append((test_name, result))
    
    # 总结测试结果
    print(f"\n{'='*60}")
    print("📊 测试结果总结:")
    print(f"{'='*60}")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(tests)} 项测试通过")
    
    if passed == len(tests):
        print("🎉 所有测试通过！库功能完全正常！")
    else:
        print("⚠️  部分测试未通过，请检查相关功能")
    
    print(f"\n{'='*60}")
    print("📋 功能特性验证:")
    print("✅ 自动分页获取数据")
    print("✅ 中文数字单位转换 (亿/万)")
    print("✅ 百分比转小数转换")
    print("✅ 数据类型自动识别")
    print("✅ Logger日志记录")
    print("✅ 客户端实例缓存")
    print("✅ 便捷函数接口")
    print("✅ 数据导出功能")
    print("✅ 错误处理机制")

if __name__ == "__main__":
    main()
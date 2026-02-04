#!/usr/bin/env python3
"""
EMXG 完整使用示例
展示东方财富股票查询库的所有主要功能
"""

import logging
from emxg import EMStockClient, search_emxg

def setup_logging():
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def basic_usage_example():
    """基本使用示例"""
    print("=" * 60)
    print("1. 基本使用示例")
    print("=" * 60)
    
    # 方法1: 使用便捷函数（推荐）
    print("\n📊 使用便捷函数查询涨停板股票:")
    df = search_emxg("今日涨停", max_count=5)
    
    if not df.empty:
        print(f"✅ 成功获取 {len(df)} 条数据")
        
        # 显示关键信息
        key_columns = ['代码', '名称', '最新价', '涨跌幅', '成交额']
        available_columns = [col for col in key_columns if col in df.columns]
        
        if available_columns:
            print("\n前5只股票:")
            for i, (_, row) in enumerate(df[available_columns].head().iterrows()):
                code = row.get('代码', 'N/A')
                name = row.get('名称', 'N/A')
                price = row.get('最新价', 'N/A')
                chg = row.get('涨跌幅', 'N/A')
                volume = row.get('成交额', 'N/A')
                
                # 格式化显示
                price_str = f"{price}元" if price != 'N/A' else 'N/A'
                chg_str = f"{chg*100:.2f}%" if isinstance(chg, (int, float)) else str(chg)
                volume_str = f"{volume/100000000:.2f}亿" if isinstance(volume, (int, float)) else str(volume)
                
                print(f"  {i+1}. {name} ({code}): {price_str}, {chg_str}, 成交额{volume_str}")
    
    # 方法2: 使用客户端类
    print("\n🔧 使用客户端类:")
    client = EMStockClient()
    df2 = client.search("今日涨停", max_count=3)
    print(f"✅ 客户端类获取 {len(df2)} 条数据")

def data_conversion_example():
    """数据转换示例"""
    print("\n" + "=" * 60)
    print("2. 数据转换功能展示")
    print("=" * 60)
    
    df = search_emxg("今日涨停", max_count=3)
    
    if not df.empty:
        print("\n💱 数据转换验证:")
        
        # 百分比转换
        if '涨跌幅' in df.columns:
            chg_val = df['涨跌幅'].iloc[0]
            print(f"  涨跌幅: {chg_val:.4f} (小数) = {chg_val*100:.2f}% (百分比)")
        
        if '换手率' in df.columns:
            turnover_val = df['换手率'].iloc[0]
            print(f"  换手率: {turnover_val:.4f} (小数) = {turnover_val*100:.2f}% (百分比)")
        
        # 数值转换
        if '成交额' in df.columns:
            volume_val = df['成交额'].iloc[0]
            print(f"  成交额: {volume_val:,.0f} 元 = {volume_val/100000000:.2f} 亿元")
        
        # 数据类型展示
        print(f"\n📋 数据类型:")
        for col in ['涨跌幅', '换手率', '成交额', '最新价']:
            if col in df.columns:
                print(f"  {col}: {df[col].dtype}")

def advanced_query_example():
    """高级查询示例"""
    print("\n" + "=" * 60)
    print("3. 高级查询功能")
    print("=" * 60)
    
    # 不同关键词查询
    keywords = [
        ("今日涨停", "涨停板股票"),
        ("涨停板首板", "首板涨停股票"),
        ("连续上涨3天", "连续上涨股票")
    ]
    
    for keyword, description in keywords:
        try:
            print(f"\n🔍 查询: {description}")
            df = search_emxg(keyword, max_count=3)
            
            if not df.empty:
                print(f"  ✅ 找到 {len(df)} 条结果")
                if '名称' in df.columns:
                    names = df['名称'].head(3).tolist()
                    print(f"  📋 股票: {', '.join(names)}")
            else:
                print(f"  ❌ 未找到相关数据")
                
        except Exception as e:
            print(f"  ⚠️  查询失败: {e}")

def data_analysis_example():
    """数据分析示例"""
    print("\n" + "=" * 60)
    print("4. 数据分析功能")
    print("=" * 60)
    
    df = search_emxg("今日涨停", max_count=10)
    
    if not df.empty:
        print(f"📊 基于 {len(df)} 条数据进行分析:")
        
        # 涨跌幅分析
        if '涨跌幅' in df.columns:
            chg_data = df['涨跌幅'].dropna()
            if not chg_data.empty:
                print(f"\n📈 涨跌幅统计:")
                print(f"  平均涨跌幅: {chg_data.mean()*100:.2f}%")
                print(f"  最高涨跌幅: {chg_data.max()*100:.2f}%")
                print(f"  最低涨跌幅: {chg_data.min()*100:.2f}%")
                
                # 涨幅分布
                high_gain = (chg_data > 0.15).sum()  # >15%
                mid_gain = ((chg_data > 0.10) & (chg_data <= 0.15)).sum()  # 10-15%
                low_gain = (chg_data <= 0.10).sum()  # ≤10%
                
                print(f"\n📊 涨幅分布:")
                print(f"  >15%: {high_gain} 只")
                print(f"  10-15%: {mid_gain} 只")
                print(f"  ≤10%: {low_gain} 只")
        
        # 成交额分析
        if '成交额' in df.columns:
            volume_data = df['成交额'].dropna()
            if not volume_data.empty:
                print(f"\n💰 成交额统计:")
                print(f"  平均成交额: {volume_data.mean()/100000000:.2f} 亿元")
                print(f"  最高成交额: {volume_data.max()/100000000:.2f} 亿元")
                print(f"  成交额>5亿: {(volume_data > 500000000).sum()} 只")
        
        # 换手率分析
        if '换手率' in df.columns:
            turnover_data = df['换手率'].dropna()
            if not turnover_data.empty:
                print(f"\n🔄 换手率统计:")
                print(f"  平均换手率: {turnover_data.mean()*100:.2f}%")
                print(f"  换手率>20%: {(turnover_data > 0.20).sum()} 只")

def data_filtering_example():
    """数据筛选示例"""
    print("\n" + "=" * 60)
    print("5. 数据筛选功能")
    print("=" * 60)
    
    df = search_emxg("今日涨停", max_count=30)
    
    if not df.empty:
        print(f"🔍 从 {len(df)} 条数据中筛选高质量股票:")
        
        # 综合筛选条件
        conditions = []
        if '涨跌幅' in df.columns:
            conditions.append(df['涨跌幅'] > 0.15)  # 涨幅>15%
        if '成交额' in df.columns:
            conditions.append(df['成交额'] > 200000000)  # 成交额>2亿
        if '换手率' in df.columns:
            conditions.append(df['换手率'] > 0.05)  # 换手率>5%
            conditions.append(df['换手率'] < 0.30)  # 换手率<30%
        
        if conditions:
            # 应用所有条件
            quality_filter = conditions[0]
            for condition in conditions[1:]:
                quality_filter = quality_filter & condition
            
            quality_stocks = df[quality_filter]
            
            print(f"✅ 筛选出 {len(quality_stocks)} 只高质量股票")
            
            if not quality_stocks.empty and '名称' in quality_stocks.columns:
                print("\n🏆 高质量股票列表:")
                for i, (_, row) in enumerate(quality_stocks.head(5).iterrows()):
                    name = row.get('名称', 'N/A')
                    code = row.get('代码', 'N/A')
                    chg = row.get('涨跌幅', 0)
                    volume = row.get('成交额', 0)
                    turnover = row.get('换手率', 0)
                    
                    print(f"  {i+1}. {name} ({code})")
                    print(f"     涨幅: {chg*100:.2f}%, 成交额: {volume/100000000:.2f}亿, 换手率: {turnover*100:.2f}%")

def data_export_example():
    """数据导出示例"""
    print("\n" + "=" * 60)
    print("6. 数据导出功能")
    print("=" * 60)
    
    df = search_emxg("今日涨停", max_count=10)
    
    if not df.empty:
        # 导出CSV
        csv_file = 'example_stocks.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✅ 数据已导出为CSV: {csv_file}")
        
        # 导出Excel（如果安装了openpyxl）
        try:
            excel_file = 'example_stocks.xlsx'
            df.to_excel(excel_file, index=False)
            print(f"✅ 数据已导出为Excel: {excel_file}")
        except ImportError:
            print("💡 提示: 安装 openpyxl 可导出Excel格式: pip install openpyxl")
        
        # 导出精简版本
        if len(df.columns) > 5:
            key_columns = ['代码', '名称', '最新价', '涨跌幅', '成交额']
            available_columns = [col for col in key_columns if col in df.columns]
            
            if available_columns:
                simple_df = df[available_columns].copy()
                simple_csv = 'example_stocks_simple.csv'
                simple_df.to_csv(simple_csv, index=False, encoding='utf-8-sig')
                print(f"✅ 精简数据已导出: {simple_csv}")

def error_handling_example():
    """错误处理示例"""
    print("\n" + "=" * 60)
    print("7. 错误处理展示")
    print("=" * 60)
    
    # 测试无效关键词
    try:
        print("🧪 测试无效关键词:")
        df = search_emxg("不存在的查询条件12345", max_count=5)
        
        if df.empty:
            print("✅ 正确处理无效关键词（返回空DataFrame）")
        else:
            print(f"⚠️  意外返回了 {len(df)} 条数据")
            
    except Exception as e:
        print(f"✅ 正确抛出异常: {type(e).__name__}: {e}")
    
    # 测试网络异常处理
    print("\n💡 提示: 库具有完善的错误处理机制")
    print("  - 网络请求失败时会自动重试")
    print("  - 数据解析错误时会给出明确提示")
    print("  - 支持详细的日志记录便于调试")

def main():
    """主函数 - 运行所有示例"""
    print("🚀 EMXG 东方财富股票查询库 - 完整功能演示")
    print("=" * 80)
    
    # 设置日志
    setup_logging()
    
    try:
        # 运行所有示例
        basic_usage_example()
        data_conversion_example()
        advanced_query_example()
        data_analysis_example()
        data_filtering_example()
        data_export_example()
        error_handling_example()
        
        print("\n" + "=" * 80)
        print("🎉 所有示例运行完成！")
        print("=" * 80)
        print("\n📚 更多功能:")
        print("  - 详细文档: 查看 README.md")
        print("  - 项目地址: https://github.com/JumuFENG/emxg")
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
    except Exception as e:
        print(f"\n❌ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
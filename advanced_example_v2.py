#!/usr/bin/env python3
"""
高级使用示例 - 新版API
展示数据自动获取、数值转换和分析功能
"""

from emxg import EMStockClient
import pandas as pd

def main():
    # 创建客户端
    client = EMStockClient()
    
    print("=== 东方财富股票查询库 v2.0 示例 ===\n")
    
    try:
        # 1. 获取所有涨停板数据（不限制数量）
        print("1. 获取所有涨停板股票数据")
        print("-" * 50)
        df_all = client.search(keyword="今日涨停", page_size=50)
        
        if not df_all.empty:
            print(f"✓ 共获取到 {len(df_all)} 条涨停板数据")
            
            # 显示数值转换效果
            if '成交额' in df_all.columns:
                print(f"✓ 成交额已转换为数值类型: {df_all['成交额'].dtype}")
                avg_volume = df_all['成交额'].mean()
                print(f"✓ 平均成交额: {avg_volume:,.0f} 元")
        
        print("\n" + "="*60 + "\n")
        
        # 2. 限制获取数量的示例
        print("2. 限制获取前30条数据")
        print("-" * 50)
        df_limited = client.search(keyword="今日涨停", page_size=20, max_count=30)
        
        if not df_limited.empty:
            print(f"✓ 限制获取到 {len(df_limited)} 条数据")
            
            # 显示关键信息
            key_columns = ['代码', '名称', '最新价', '涨跌幅', '成交额', '换手率']
            available_columns = [col for col in key_columns if col in df_limited.columns]
            
            print("\n前10只股票:")
            display_df = df_limited[available_columns].head(10).copy()
            
            # 格式化显示
            if '成交额' in display_df.columns:
                display_df['成交额(万元)'] = display_df['成交额'].apply(
                    lambda x: f"{x/10000:,.0f}" if pd.notna(x) else "N/A"
                )
                display_df = display_df.drop('成交额', axis=1)
            
            print(display_df.to_string(index=False))
        
        print("\n" + "="*60 + "\n")
        
        # 3. 数据分析示例
        print("3. 数据分析")
        print("-" * 50)
        
        if not df_all.empty:
            # 涨跌幅分析
            if '涨跌幅' in df_all.columns:
                chg_data = df_all['涨跌幅'].dropna()
                if not chg_data.empty:
                    print(f"涨跌幅统计:")
                    print(f"  平均涨跌幅: {chg_data.mean()*100:.2f}%")
                    print(f"  最高涨跌幅: {chg_data.max()*100:.2f}%")
                    print(f"  最低涨跌幅: {chg_data.min()*100:.2f}%")
                    
                    # 涨幅分布（注意：数据已经是小数形式）
                    high_gain = (chg_data > 0.15).sum()  # >15%
                    mid_gain = ((chg_data > 0.10) & (chg_data <= 0.15)).sum()  # 10-15%
                    low_gain = (chg_data <= 0.10).sum()  # ≤10%
                    
                    print(f"\n涨幅分布:")
                    print(f"  >15%: {high_gain} 只")
                    print(f"  10-15%: {mid_gain} 只") 
                    print(f"  ≤10%: {low_gain} 只")
            
            # 成交额分析
            if '成交额' in df_all.columns:
                volume_data = df_all['成交额'].dropna()
                if not volume_data.empty:
                    print(f"\n成交额统计:")
                    print(f"  平均成交额: {volume_data.mean()/100000000:.2f} 亿元")
                    print(f"  最高成交额: {volume_data.max()/100000000:.2f} 亿元")
                    print(f"  成交额>5亿的股票: {(volume_data > 500000000).sum()} 只")
            
            # 换手率分析
            if '换手率' in df_all.columns:
                turnover_data = df_all['换手率'].dropna()
                if not turnover_data.empty:
                    print(f"\n换手率统计:")
                    print(f"  平均换手率: {turnover_data.mean()*100:.2f}%")
                    print(f"  换手率>20%的股票: {(turnover_data > 0.20).sum()} 只")
        
        print("\n" + "="*60 + "\n")
        
        # 4. 不同关键词查询对比
        print("4. 不同关键词查询对比")
        print("-" * 50)
        
        keywords = ["今日涨停", "涨停板首板"]
        
        for keyword in keywords:
            try:
                print(f"\n查询关键词: '{keyword}'")
                df_test = client.search(keyword=keyword, page_size=10, max_count=10)
                
                if not df_test.empty:
                    print(f"  找到 {len(df_test)} 条结果")
                    if '名称' in df_test.columns and '涨跌幅' in df_test.columns:
                        print("  前5只股票:")
                        for i, (_, row) in enumerate(df_test.head().iterrows()):
                            name = row.get('名称', 'N/A')
                            code = row.get('代码', 'N/A')
                            chg = row.get('涨跌幅', 'N/A')
                            # 将小数转换回百分比显示
                            chg_display = f"{chg*100:.2f}%" if pd.notna(chg) and isinstance(chg, (int, float)) else f"{chg}%"
                            print(f"    {i+1}. {name} ({code}): {chg_display}")
                else:
                    print("  未找到相关数据")
                    
            except Exception as e:
                print(f"  查询 '{keyword}' 失败: {e}")
        
        print("\n" + "="*60 + "\n")
        
        # 5. 数据保存
        print("5. 数据保存")
        print("-" * 50)
        
        if not df_all.empty:
            # 保存完整数据
            df_all.to_csv('all_limit_up_stocks.csv', index=False, encoding='utf-8-sig')
            print("✓ 完整数据已保存为: all_limit_up_stocks.csv")
            
            # 保存精简数据
            if len(available_columns) > 0:
                df_simple = df_all[available_columns].copy()
                df_simple.to_csv('simple_stocks.csv', index=False, encoding='utf-8-sig')
                print("✓ 精简数据已保存为: simple_stocks.csv")
            
            # 保存高质量股票（成交额>2亿且换手率>5%）
            if '成交额' in df_all.columns and '换手率' in df_all.columns:
                high_quality = df_all[
                    (df_all['成交额'] > 200000000) & 
                    (df_all['换手率'] > 0.05)  # 5% = 0.05
                ].copy()
                
                if not high_quality.empty:
                    high_quality.to_csv('high_quality_stocks.csv', index=False, encoding='utf-8-sig')
                    print(f"✓ 高质量股票({len(high_quality)}只)已保存为: high_quality_stocks.csv")
        
        print(f"\n🎉 查询完成！")
        
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
浏览器指纹生成示例
展示如何使用get_printfinger函数
"""

from emxg import get_printfinger
from emxg.emfinger import EMFingerprint

def basic_fingerprint_example():
    """基本指纹生成示例"""
    print("🔍 基本浏览器指纹生成")
    print("=" * 40)
    
    # 使用便捷函数生成指纹
    fingerprint = get_printfinger()
    print(f"生成的指纹: {fingerprint}")
    print(f"指纹长度: {len(fingerprint)} 字符")
    
    # 多次生成查看一致性
    print("\n🔄 多次生成测试:")
    for i in range(3):
        fp = get_printfinger()
        print(f"第{i+1}次: {fp}")

def custom_options_example():
    """自定义选项示例"""
    print("\n⚙️ 自定义选项指纹生成")
    print("=" * 40)
    
    # 排除用户代理
    options1 = {'excludeUserAgent': True}
    fp1 = get_printfinger(options1)
    print(f"排除用户代理: {fp1}")
    
    # 排除Canvas和WebGL
    options2 = {'excludeCanvas': True, 'excludeWebGL': True}
    fp2 = get_printfinger(options2)
    print(f"排除Canvas/WebGL: {fp2}")
    
    # 排除多个选项
    options3 = {
        'excludeUserAgent': True,
        'excludeLanguage': True,
        'excludeCanvas': True,
        'excludePlugins': True
    }
    fp3 = get_printfinger(options3)
    print(f"排除多个选项: {fp3}")

def detailed_fingerprint_example():
    """详细指纹信息示例"""
    print("\n📊 详细指纹信息")
    print("=" * 40)
    
    # 创建指纹实例
    fp = EMFingerprint()
    
    # 显示各个组件
    print("指纹组件:")
    print(f"  用户代理: {fp.get_user_agent()}")
    print(f"  语言: {fp.get_language()}")
    print(f"  颜色深度: {fp.get_color_depth()}")
    print(f"  像素比: {fp.get_pixel_ratio()}")
    print(f"  屏幕分辨率: {fp.get_screen_resolution()}")
    print(f"  时区偏移: {fp.get_timezone_offset()}")
    print(f"  平台: {fp.get_platform()}")
    print(f"  CPU类别: {fp.get_cpu_class()}")
    print(f"  硬件并发: {fp.get_hardware_concurrency()}")
    print(f"  触摸支持: {fp.get_touch_support()}")
    
    # 显示字体信息（只显示前10个）
    fonts = fp.get_fonts()
    print(f"  字体数量: {len(fonts)}")
    print(f"  前10个字体: {fonts[:10]}")
    
    # 生成最终指纹
    final_fp = fp.generate_fingerprint()
    print(f"\n最终指纹: {final_fp}")

def fingerprint_data_collection_example():
    """指纹数据收集示例"""
    print("\n📋 指纹数据收集")
    print("=" * 40)
    
    fp = EMFingerprint()
    data = fp.collect_fingerprint_data()
    
    print(f"收集到 {len(data)} 个数据项:")
    for item in data[:10]:  # 只显示前10个
        key = item['key']
        value = item['value']
        if isinstance(value, list):
            value_str = f"[{len(value)} items]"
        elif isinstance(value, str) and len(value) > 50:
            value_str = f"{value[:50]}..."
        else:
            value_str = str(value)
        print(f"  {key}: {value_str}")
    
    if len(data) > 10:
        print(f"  ... 还有 {len(data) - 10} 个数据项")

def comparison_example():
    """指纹对比示例"""
    print("\n🔍 指纹对比")
    print("=" * 40)
    
    # 默认配置
    fp1 = get_printfinger()
    print(f"默认配置: {fp1}")
    
    # 不同配置
    configs = [
        ({'excludeUserAgent': True}, "排除用户代理"),
        ({'excludeCanvas': True}, "排除Canvas"),
        ({'excludeWebGL': True}, "排除WebGL"),
        ({'excludePlugins': True}, "排除插件"),
    ]
    
    for config, desc in configs:
        fp = get_printfinger(config)
        is_different = fp != fp1
        status = "✓ 不同" if is_different else "✗ 相同"
        print(f"{desc}: {fp} {status}")

def main():
    """主函数"""
    print("🔐 浏览器指纹生成器示例")
    print("=" * 60)
    
    try:
        basic_fingerprint_example()
        custom_options_example()
        detailed_fingerprint_example()
        fingerprint_data_collection_example()
        comparison_example()
        
        print("\n" + "=" * 60)
        print("🎉 指纹生成示例完成！")
        print("\n💡 使用场景:")
        print("  - 设备识别和追踪")
        print("  - 反爬虫和安全验证")
        print("  - 用户行为分析")
        print("  - 浏览器环境模拟")
        
        print("\n⚠️ 注意事项:")
        print("  - 指纹可能因系统环境而异")
        print("  - 某些组件包含随机元素")
        print("  - 建议根据需要调整配置选项")
        
    except Exception as e:
        print(f"❌ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
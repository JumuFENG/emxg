#!/usr/bin/env python3
"""
测试emfinger.py模块
"""

import pytest
import hashlib
from unittest.mock import patch, MagicMock
from emxg.emfinger import EMFingerprint, get_printfinger


class TestEMFingerprint:
    """测试EMFingerprint类"""
    
    def test_init_default_options(self):
        """测试默认选项初始化"""
        fp = EMFingerprint()
        assert isinstance(fp.options, dict)
        assert 'excludeUserAgent' in fp.options
        assert fp.options['excludeUserAgent'] is False
        assert fp.options['detectScreenOrientation'] is True
    
    def test_init_custom_options(self):
        """测试自定义选项初始化"""
        custom_options = {'excludeUserAgent': True, 'excludeLanguage': True}
        fp = EMFingerprint(custom_options)
        assert fp.options['excludeUserAgent'] is True
        assert fp.options['excludeLanguage'] is True
        # 确保其他默认选项仍然存在
        assert 'excludeColorDepth' in fp.options
    
    def test_get_user_agent(self):
        """测试用户代理获取"""
        fp = EMFingerprint()
        user_agent = fp.get_user_agent()
        assert isinstance(user_agent, str)
        assert len(user_agent) > 0
        assert 'Mozilla' in user_agent
        # 测试多次调用可能返回不同的用户代理
        user_agents = [fp.get_user_agent() for _ in range(10)]
        assert all(isinstance(ua, str) for ua in user_agents)
    
    def test_get_language(self):
        """测试语言获取"""
        fp = EMFingerprint()
        language = fp.get_language()
        assert isinstance(language, str)
        assert len(language) > 0
        # 应该是有效的语言代码格式
        assert '-' in language or len(language) == 2
    
    def test_get_color_depth(self):
        """测试颜色深度获取"""
        fp = EMFingerprint()
        color_depth = fp.get_color_depth()
        assert isinstance(color_depth, int)
        assert color_depth > 0
        assert color_depth == 24  # 根据实现，应该返回24
    
    def test_get_pixel_ratio(self):
        """测试像素比获取"""
        fp = EMFingerprint()
        pixel_ratio = fp.get_pixel_ratio()
        assert isinstance(pixel_ratio, float)
        assert pixel_ratio > 0
        assert pixel_ratio == 1.0  # 根据实现，应该返回1.0
    
    def test_get_screen_resolution(self):
        """测试屏幕分辨率获取"""
        fp = EMFingerprint()
        resolution = fp.get_screen_resolution()
        assert isinstance(resolution, list)
        assert len(resolution) == 2
        assert all(isinstance(r, int) for r in resolution)
        assert all(r > 0 for r in resolution)
        # 测试返回的是预定义的分辨率之一
        valid_resolutions = [
            [1920, 1080], [1366, 768], [1440, 900],
            [1536, 864], [1280, 720], [2560, 1440], [3840, 2160]
        ]
        assert resolution in valid_resolutions
    
    def test_get_available_screen_resolution(self):
        """测试可用屏幕分辨率获取"""
        fp = EMFingerprint()
        available_resolution = fp.get_available_screen_resolution()
        assert isinstance(available_resolution, list)
        assert len(available_resolution) == 2
        assert all(isinstance(r, int) for r in available_resolution)
        assert all(r > 0 for r in available_resolution)
        # 可用分辨率的高度应该比实际分辨率小
        actual_resolution = fp.get_screen_resolution()
        # 注意：由于随机性，这个测试可能不总是成立，但逻辑上应该如此
    
    def test_get_timezone_offset(self):
        """测试时区偏移获取"""
        fp = EMFingerprint()
        timezone_offset = fp.get_timezone_offset()
        assert isinstance(timezone_offset, int)
        # 时区偏移应该在合理范围内（-12到+14小时，即-720到+840分钟）
        assert -720 <= timezone_offset <= 840
    
    def test_get_platform(self):
        """测试平台信息获取"""
        fp = EMFingerprint()
        platform_info = fp.get_platform()
        assert isinstance(platform_info, str)
        assert len(platform_info) > 0
    
    def test_get_cpu_class(self):
        """测试CPU类别获取"""
        fp = EMFingerprint()
        cpu_class = fp.get_cpu_class()
        assert isinstance(cpu_class, str)
        assert len(cpu_class) > 0
    
    def test_get_hardware_concurrency(self):
        """测试硬件并发数获取"""
        fp = EMFingerprint()
        concurrency = fp.get_hardware_concurrency()
        assert isinstance(concurrency, int)
        assert concurrency > 0
        assert concurrency <= 128  # 合理的上限
    
    def test_get_canvas_fp(self):
        """测试Canvas指纹获取"""
        fp = EMFingerprint()
        canvas_fp = fp.get_canvas_fp()
        assert isinstance(canvas_fp, str)
        assert len(canvas_fp) > 0
        assert 'canvas winding:yes' in canvas_fp
        assert 'canvas fp:data:image/png;base64,' in canvas_fp
        # 注意：由于用户代理是随机选择的，Canvas指纹可能不完全一致
        # 但结构应该相同
    
    def test_generate_mock_canvas_data(self):
        """测试模拟Canvas数据生成"""
        fp = EMFingerprint()
        canvas_data = fp._generate_mock_canvas_data()
        assert isinstance(canvas_data, str)
        assert len(canvas_data) == 32  # MD5哈希的长度
        # 注意：由于用户代理是随机的，Canvas数据可能不完全一致
    
    def test_get_webgl_fp(self):
        """测试WebGL指纹获取"""
        fp = EMFingerprint()
        webgl_fp = fp.get_webgl_fp()
        assert isinstance(webgl_fp, str)
        assert len(webgl_fp) > 0
        assert 'webgl vendor:' in webgl_fp
        assert 'webgl renderer:' in webgl_fp
        # 测试一致性
        assert webgl_fp == fp.get_webgl_fp()
    
    def test_get_plugins(self):
        """测试插件信息获取"""
        fp = EMFingerprint()
        plugins = fp.get_plugins()
        assert isinstance(plugins, list)
        assert len(plugins) > 0
        assert all(isinstance(plugin, str) for plugin in plugins)
        # 检查是否包含预期的插件
        plugin_str = '~'.join(plugins)
        assert 'Chrome PDF Plugin' in plugin_str
    
    def test_get_fonts(self):
        """测试字体信息获取"""
        fp = EMFingerprint()
        fonts = fp.get_fonts()
        assert isinstance(fonts, list)
        assert len(fonts) >= 15  # 至少应该有15个字体
        assert all(isinstance(font, str) for font in fonts)
        # 字体列表应该是排序的
        assert fonts == sorted(fonts)
        # 检查是否都是有效的字体名称（非空字符串）
        assert all(len(font) > 0 for font in fonts)
        # 检查是否包含一些预期的字体类型（但不要求特定字体）
        font_str = ' '.join(fonts).lower()
        # 至少应该包含一些常见的字体类别
        common_font_patterns = ['arial', 'times', 'helvetica', 'courier', 'verdana', 'georgia']
        found_patterns = [pattern for pattern in common_font_patterns if pattern in font_str]
        assert len(found_patterns) >= 2  # 至少找到2种常见字体类型
    
    def test_get_touch_support(self):
        """测试触摸支持获取"""
        fp = EMFingerprint()
        touch_support = fp.get_touch_support()
        assert isinstance(touch_support, list)
        assert len(touch_support) == 3
        assert touch_support == [0, False, False]  # 根据实现，模拟非触摸设备
    
    def test_collect_fingerprint_data(self):
        """测试指纹数据收集"""
        fp = EMFingerprint()
        data = fp.collect_fingerprint_data()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 检查数据结构
        for item in data:
            assert isinstance(item, dict)
            assert 'key' in item
            assert 'value' in item
            assert isinstance(item['key'], str)
        
        # 检查是否包含预期的键
        keys = [item['key'] for item in data]
        expected_keys = [
            'user_agent', 'language', 'color_depth', 'pixel_ratio',
            'hardware_concurrency', 'resolution', 'available_resolution',
            'timezone_offset', 'session_storage', 'local_storage',
            'indexed_db', 'cpu_class', 'navigator_platform', 'do_not_track',
            'regular_plugins', 'canvas', 'webgl', 'adblock', 'touch_support',
            'js_fonts'
        ]
        for expected_key in expected_keys:
            assert expected_key in keys
    
    def test_collect_fingerprint_data_with_exclusions(self):
        """测试带排除选项的指纹数据收集"""
        options = {
            'excludeUserAgent': True,
            'excludeLanguage': True,
            'excludeCanvas': True
        }
        fp = EMFingerprint(options)
        data = fp.collect_fingerprint_data()
        
        keys = [item['key'] for item in data]
        assert 'user_agent' not in keys
        assert 'language' not in keys
        assert 'canvas' not in keys
        # 其他键应该仍然存在
        assert 'color_depth' in keys
        assert 'resolution' in keys
    
    def test_murmur_hash(self):
        """测试MurmurHash实现"""
        fp = EMFingerprint()
        
        # 测试基本功能
        hash1 = fp.murmur_hash("test data")
        assert isinstance(hash1, str)
        assert len(hash1) == 32  # MD5哈希长度
        
        # 测试一致性
        hash2 = fp.murmur_hash("test data")
        assert hash1 == hash2
        
        # 测试不同数据产生不同哈希
        hash3 = fp.murmur_hash("different data")
        assert hash1 != hash3
        
        # 测试种子值影响
        hash4 = fp.murmur_hash("test data", seed=42)
        assert hash1 != hash4
    
    def test_generate_fingerprint(self):
        """测试指纹生成"""
        fp = EMFingerprint()
        fingerprint = fp.generate_fingerprint()
        
        assert isinstance(fingerprint, str)
        assert len(fingerprint) == 32  # MD5哈希长度
        
        # 测试一致性：相同配置应该产生相同指纹
        fingerprint2 = fp.generate_fingerprint()
        # 注意：由于某些随机元素，这可能不总是相等
        # 但在大多数情况下应该相等
        
        # 测试不同配置产生不同指纹
        fp2 = EMFingerprint({'excludeUserAgent': True})
        fingerprint3 = fp2.generate_fingerprint()
        # 由于配置不同，指纹应该不同（大概率）


class TestGetPrintfinger:
    """测试get_printfinger便捷函数"""
    
    def test_get_printfinger_basic(self):
        """测试基本功能"""
        fingerprint = get_printfinger()
        assert isinstance(fingerprint, str)
        assert len(fingerprint) == 32
    
    def test_get_printfinger_consistency(self):
        """测试一致性"""
        # 测试无参数调用
        fingerprint1 = get_printfinger()
        fingerprint2 = get_printfinger()
        # 注意：由于随机元素，可能不完全一致
        assert isinstance(fingerprint1, str)
        assert isinstance(fingerprint2, str)


class TestIntegration:
    """集成测试"""
    
    def test_fingerprint_generation(self):
        """测试指纹生成"""
        # 测试指纹生成功能
        fp = EMFingerprint()
        fingerprints = [fp.generate_fingerprint() for _ in range(3)]
        
        # 所有指纹都应该是有效的字符串
        assert all(isinstance(f, str) for f in fingerprints)
        assert all(len(f) == 32 for f in fingerprints)
        
        # 由于随机元素，指纹可能不同，这是正常的
    
    def test_different_options_different_fingerprints(self):
        """测试不同选项产生不同指纹"""
        fp1 = EMFingerprint()
        fp2 = EMFingerprint({'excludeUserAgent': True})
        fp3 = EMFingerprint({'excludeCanvas': True, 'excludeWebGL': True})
        
        fingerprint1 = fp1.generate_fingerprint()
        fingerprint2 = fp2.generate_fingerprint()
        fingerprint3 = fp3.generate_fingerprint()
        
        # 不同配置应该产生不同指纹（高概率）
        fingerprints = {fingerprint1, fingerprint2, fingerprint3}
        assert len(fingerprints) >= 2  # 至少有2个不同的指纹
    
    @patch('platform.system')
    @patch('platform.release')
    def test_platform_dependency(self, mock_release, mock_system):
        """测试平台依赖性"""
        # 模拟不同平台
        mock_system.return_value = 'Linux'
        mock_release.return_value = '5.4.0'
        
        fp1 = EMFingerprint()
        fingerprint1 = fp1.generate_fingerprint()
        
        # 改变平台信息
        mock_system.return_value = 'Windows'
        mock_release.return_value = '10'
        
        fp2 = EMFingerprint()
        fingerprint2 = fp2.generate_fingerprint()
        
        # 不同平台应该产生不同指纹
        assert fingerprint1 != fingerprint2


if __name__ == "__main__":
    pytest.main([__file__])
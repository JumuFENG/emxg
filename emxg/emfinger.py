#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器指纹生成器 - Python实现
基于JavaScript fingerprint.js的实现原理
"""

import hashlib
import json
import platform
import time
import locale
import random
from typing import Dict, List, Any, Optional
from functools import lru_cache


class EMFingerprint:
    """浏览器指纹生成器"""

    def __init__(self, options: Optional[Dict] = None):
        """
        初始化指纹生成器

        Args:
            options: 配置选项
        """
        default_options = {
            'excludeUserAgent': False,
            'excludeLanguage': False,
            'excludeColorDepth': False,
            'excludePixelRatio': False,
            'excludeScreenResolution': False,
            'excludeAvailableScreenResolution': False,
            'excludeTimezoneOffset': False,
            'excludeSessionStorage': False,
            'excludeLocalStorage': False,
            'excludeIndexedDB': False,
            'excludeAddBehavior': False,
            'excludeOpenDatabase': False,
            'excludeCpuClass': False,
            'excludePlatform': False,
            'excludeDoNotTrack': False,
            'excludeCanvas': False,
            'excludeWebGL': False,
            'excludeAdBlock': False,
            'excludePlugins': False,
            'excludeHasLiedLanguages': False,
            'excludeHasLiedResolution': False,
            'excludeHasLiedOs': False,
            'excludeHasLiedBrowser': False,
            'excludeTouchSupport': False,
            'detectScreenOrientation': True,
        }

        self.options = default_options
        if options:
            self.options.update(options)

    def get_user_agent(self) -> str:
        """获取用户代理字符串"""
        # 模拟常见的浏览器User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        return random.choice(user_agents)

    def get_language(self) -> str:
        """获取语言设置"""
        try:
            # 使用更现代的方法获取语言设置
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                lang = locale.getdefaultlocale()[0]
            if lang:
                return lang.replace('_', '-')
        except:
            pass
        return 'zh-CN'

    def get_color_depth(self) -> int:
        """获取颜色深度"""
        # 大多数现代显示器都是24位色深
        return 24

    def get_pixel_ratio(self) -> float:
        """获取像素比"""
        # 大多数显示器的像素比为1.0，高分辨率显示器可能是2.0或更高
        return 1.0

    def get_screen_resolution(self) -> List[int]:
        """获取屏幕分辨率"""
        # 模拟常见的屏幕分辨率
        resolutions = [
            [1920, 1080],
            [1366, 768],
            [1440, 900],
            [1536, 864],
            [1280, 720],
            [2560, 1440],
            [3840, 2160]
        ]
        return random.choice(resolutions)

    def get_available_screen_resolution(self) -> List[int]:
        """获取可用屏幕分辨率"""
        resolution = self.get_screen_resolution()
        # 可用分辨率通常比实际分辨率小一些（减去任务栏等）
        return [resolution[0], resolution[1] - 40]

    def get_timezone_offset(self) -> int:
        """获取时区偏移"""
        # 返回与UTC的分钟差
        return int(time.timezone / 60)

    def get_platform(self) -> str:
        """获取平台信息"""
        return platform.platform()

    def get_cpu_class(self) -> str:
        """获取CPU类别"""
        return platform.processor() or platform.machine() or 'unknown'

    def get_hardware_concurrency(self) -> int:
        """获取硬件并发数"""
        try:
            import os
            return os.cpu_count() or 4
        except:
            return 4

    def get_canvas_fp(self) -> str:
        """获取Canvas指纹"""
        # 模拟Canvas指纹生成
        # 在实际浏览器环境中，这会基于Canvas渲染结果生成唯一指纹
        canvas_data = [
            "canvas winding:yes",
            f"canvas fp:data:image/png;base64,{self._generate_mock_canvas_data()}"
        ]
        return "~".join(canvas_data)

    def _generate_mock_canvas_data(self) -> str:
        """生成模拟的Canvas数据"""
        # 基于系统信息生成一个相对稳定的Canvas指纹
        system_info = f"{platform.system()}{platform.release()}{self.get_user_agent()}"
        return hashlib.md5(system_info.encode()).hexdigest()[:32]

    def get_webgl_fp(self) -> Optional[str]:
        """获取WebGL指纹"""
        # 模拟WebGL指纹
        webgl_data = [
            "webgl vendor:Google Inc. (Intel)",
            "webgl renderer:ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "webgl version:WebGL 1.0 (OpenGL ES 2.0 Chromium)",
            "webgl shading language version:WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
            "webgl aliased line width range:[1, 1]",
            "webgl aliased point size range:[1, 1024]",
            "webgl alpha bits:8",
            "webgl antialiasing:yes",
            "webgl blue bits:8",
            "webgl depth bits:24",
            "webgl green bits:8",
            "webgl max anisotropy:16",
            "webgl max combined texture image units:32",
            "webgl max cube map texture size:16384",
            "webgl max fragment uniform vectors:1024",
            "webgl max render buffer size:16384",
            "webgl max texture image units:16",
            "webgl max texture size:16384",
            "webgl max varying vectors:30",
            "webgl max vertex attribs:16",
            "webgl max vertex texture image units:16",
            "webgl max vertex uniform vectors:4095",
            "webgl max viewport dims:[32767, 32767]",
            "webgl red bits:8",
            "webgl renderer:ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "webgl shading language version:WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
            "webgl stencil bits:0",
            "webgl vendor:Google Inc. (Intel)",
            "webgl version:WebGL 1.0 (OpenGL ES 2.0 Chromium)",
            "webgl vertex shader high float precision:23",
            "webgl vertex shader high float precision rangeMin:127",
            "webgl vertex shader high float precision rangeMax:127",
            "webgl vertex shader medium float precision:23",
            "webgl vertex shader medium float precision rangeMin:127",
            "webgl vertex shader medium float precision rangeMax:127",
            "webgl vertex shader low float precision:23",
            "webgl vertex shader low float precision rangeMin:127",
            "webgl vertex shader low float precision rangeMax:127",
            "webgl fragment shader high float precision:23",
            "webgl fragment shader high float precision rangeMin:127",
            "webgl fragment shader high float precision rangeMax:127",
            "webgl fragment shader medium float precision:23",
            "webgl fragment shader medium float precision rangeMin:127",
            "webgl fragment shader medium float precision rangeMax:127",
            "webgl fragment shader low float precision:23",
            "webgl fragment shader low float precision rangeMin:127",
            "webgl fragment shader low float precision rangeMax:127",
            "webgl vertex shader high int precision:0",
            "webgl vertex shader high int precision rangeMin:31",
            "webgl vertex shader high int precision rangeMax:30",
            "webgl vertex shader medium int precision:0",
            "webgl vertex shader medium int precision rangeMin:31",
            "webgl vertex shader medium int precision rangeMax:30",
            "webgl vertex shader low int precision:0",
            "webgl vertex shader low int precision rangeMin:31",
            "webgl vertex shader low int precision rangeMax:30",
            "webgl fragment shader high int precision:0",
            "webgl fragment shader high int precision rangeMin:31",
            "webgl fragment shader high int precision rangeMax:30",
            "webgl fragment shader medium int precision:0",
            "webgl fragment shader medium int precision rangeMin:31",
            "webgl fragment shader medium int precision rangeMax:30",
            "webgl fragment shader low int precision:0",
            "webgl fragment shader low int precision rangeMin:31",
            "webgl fragment shader low int precision rangeMax:30"
        ]
        return "~".join(webgl_data)

    def get_plugins(self) -> List[str]:
        """获取插件信息"""
        # 模拟常见的浏览器插件
        plugins = [
            "Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf",
            "Chrome PDF Viewer::::application/pdf~pdf",
            "Native Client::::application/x-nacl~,application/x-pnacl~"
        ]
        return plugins

    def get_fonts(self) -> List[str]:
        """获取字体信息"""
        # 模拟常见的系统字体
        fonts = [
            "Arial", "Arial Black", "Arial Narrow", "Arial Unicode MS",
            "Calibri", "Cambria", "Cambria Math", "Comic Sans MS",
            "Consolas", "Courier", "Courier New", "Georgia",
            "Helvetica", "Impact", "Lucida Console", "Lucida Sans Unicode",
            "Microsoft Sans Serif", "Palatino Linotype", "Segoe UI",
            "Tahoma", "Times", "Times New Roman", "Trebuchet MS",
            "Verdana", "Webdings", "Wingdings"
        ]
        # 随机选择一些字体，模拟不同系统的字体差异
        available_fonts = random.sample(fonts, random.randint(15, len(fonts)))
        return sorted(available_fonts)

    def get_touch_support(self) -> List:
        """获取触摸支持信息"""
        # [maxTouchPoints, touchEvent, touchStart]
        return [0, False, False]  # 模拟非触摸设备

    def collect_fingerprint_data(self) -> List[Dict[str, Any]]:
        """收集指纹数据"""
        data = []

        # 用户代理
        if not self.options.get('excludeUserAgent'):
            data.append({
                'key': 'user_agent',
                'value': self.get_user_agent()
            })

        # 语言
        if not self.options.get('excludeLanguage'):
            data.append({
                'key': 'language',
                'value': self.get_language()
            })

        # 颜色深度
        if not self.options.get('excludeColorDepth'):
            data.append({
                'key': 'color_depth',
                'value': self.get_color_depth()
            })

        # 像素比
        if not self.options.get('excludePixelRatio'):
            data.append({
                'key': 'pixel_ratio',
                'value': self.get_pixel_ratio()
            })

        # 硬件并发
        data.append({
            'key': 'hardware_concurrency',
            'value': self.get_hardware_concurrency()
        })

        # 屏幕分辨率
        if not self.options.get('excludeScreenResolution'):
            data.append({
                'key': 'resolution',
                'value': self.get_screen_resolution()
            })

        # 可用屏幕分辨率
        if not self.options.get('excludeAvailableScreenResolution'):
            data.append({
                'key': 'available_resolution',
                'value': self.get_available_screen_resolution()
            })

        # 时区偏移
        if not self.options.get('excludeTimezoneOffset'):
            data.append({
                'key': 'timezone_offset',
                'value': self.get_timezone_offset()
            })

        # 会话存储
        if not self.options.get('excludeSessionStorage'):
            data.append({
                'key': 'session_storage',
                'value': 1
            })

        # 本地存储
        if not self.options.get('excludeLocalStorage'):
            data.append({
                'key': 'local_storage',
                'value': 1
            })

        # IndexedDB
        if not self.options.get('excludeIndexedDB'):
            data.append({
                'key': 'indexed_db',
                'value': 1
            })

        # CPU类别
        if not self.options.get('excludeCpuClass'):
            data.append({
                'key': 'cpu_class',
                'value': self.get_cpu_class()
            })

        # 平台
        if not self.options.get('excludePlatform'):
            data.append({
                'key': 'navigator_platform',
                'value': self.get_platform()
            })

        # Do Not Track
        if not self.options.get('excludeDoNotTrack'):
            data.append({
                'key': 'do_not_track',
                'value': 'unknown'
            })

        # 插件
        if not self.options.get('excludePlugins'):
            data.append({
                'key': 'regular_plugins',
                'value': self.get_plugins()
            })

        # Canvas指纹
        if not self.options.get('excludeCanvas'):
            data.append({
                'key': 'canvas',
                'value': self.get_canvas_fp()
            })

        # WebGL指纹
        if not self.options.get('excludeWebGL'):
            webgl_fp = self.get_webgl_fp()
            if webgl_fp:
                data.append({
                    'key': 'webgl',
                    'value': webgl_fp
                })

        # 广告拦截
        if not self.options.get('excludeAdBlock'):
            data.append({
                'key': 'adblock',
                'value': False
            })

        # 触摸支持
        if not self.options.get('excludeTouchSupport'):
            data.append({
                'key': 'touch_support',
                'value': self.get_touch_support()
            })

        # 字体
        data.append({
            'key': 'js_fonts',
            'value': self.get_fonts()
        })

        return data

    def murmur_hash(self, data: str, seed: int = 31) -> str:
        """
        简化的MurmurHash实现

        Args:
            data: 要哈希的数据
            seed: 种子值

        Returns:
            哈希值的十六进制字符串
        """
        # 使用Python的hashlib作为替代实现
        # 在实际应用中，可以实现完整的MurmurHash算法
        hash_input = f"{data}_{seed}".encode('utf-8')
        return hashlib.md5(hash_input).hexdigest()

    def generate_fingerprint(self) -> str:
        """
        生成浏览器指纹

        Returns:
            指纹哈希值
        """
        # 收集指纹数据
        fingerprint_data = self.collect_fingerprint_data()

        # 将数据转换为字符串
        values = []
        for item in fingerprint_data:
            value = item['value']
            if isinstance(value, list):
                value = ';'.join(map(str, value))
            elif not isinstance(value, str):
                value = str(value)
            values.append(value)

        # 连接所有值
        combined_data = '~~~'.join(values)

        # 生成哈希
        return self.murmur_hash(combined_data, 31)

@lru_cache(maxsize=1)
def get_printfinger() -> str:
    """
    获取浏览器指纹的便捷函数

    Returns:
        浏览器指纹哈希值
    """
    fingerprint = EMFingerprint()
    return fingerprint.generate_fingerprint()

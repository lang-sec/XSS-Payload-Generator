"""
Payload管理核心模块
负责payload的加载、筛选、变异等核心逻辑
"""
import json
import os
from xss_payload_generator import XSSPayloadGenerator


class PayloadManager:
    """Payload管理器"""

    def __init__(self):
        self.generator = XSSPayloadGenerator()
        self.custom_payloads_file = 'custom_payloads.json'
        self.custom_payloads = []
        self.load_custom_payloads()

    def get_all_categories(self):
        """获取所有类别"""
        return [
            "基础Payload",
            "无交互自动触发",
            "需交互触发",
            "JavaScript上下文",
            "属性逃逸",
            "编码绕过",
            "函数绕过",
            "WAF绕过技巧",
            "SVG技巧",
            "框架特定",
            "长度限制",
            "严格绕过"
        ]

    def get_payloads_by_category(self, category):
        """根据类别获取payload"""
        category_map = {
            "基础Payload": self.generator.base_payloads,
            "无交互自动触发": self.generator.auto_trigger,
            "需交互触发": self.generator.interactive,
            "JavaScript上下文": self.generator.js_context,
            "属性逃逸": self.generator.attr_escape,
            "编码绕过": self.generator.encoding_bypass,
            "函数绕过": self.generator.function_bypass,
            "WAF绕过技巧": self.generator.waf_bypass,
            "SVG技巧": self.generator.svg_tricks,
            "框架特定": self.generator.framework,
            "长度限制": self.generator.short_payloads,
            "严格绕过": self.generator.strict_bypass,
        }
        return category_map.get(category, {})

    def load_custom_payloads(self):
        """加载自定义payload"""
        try:
            if os.path.exists(self.custom_payloads_file):
                with open(self.custom_payloads_file, 'r', encoding='utf-8') as f:
                    self.custom_payloads = json.load(f)
        except Exception as e:
            print(f"加载自定义payload失败: {e}")
            self.custom_payloads = []

    def save_custom_payloads(self):
        """保存自定义payload"""
        try:
            with open(self.custom_payloads_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_payloads, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存自定义payload失败: {e}")
            return False

    def add_custom_payload(self, name, source, payload):
        """添加自定义payload"""
        self.custom_payloads.append({
            'name': name,
            'source': source,
            'code': payload  # 使用code字段以兼容原版
        })
        return self.save_custom_payloads()

    def delete_custom_payload(self, index):
        """删除自定义payload"""
        if 0 <= index < len(self.custom_payloads):
            self.custom_payloads.pop(index)
            return self.save_custom_payloads()
        return False

    def get_custom_payloads(self):
        """获取所有自定义payload"""
        return self.custom_payloads

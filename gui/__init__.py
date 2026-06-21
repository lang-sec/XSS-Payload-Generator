"""
GUI基础模块 - 包含所有GUI相关的导入
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from custom_checkbox import CustomCheckBox
from themes import get_global_stylesheet, THEMES
from knowledge_content import get_knowledge_html


def get_styles(theme_name='light'):
    """获取样式表（兼容层）"""
    return {
        'global': get_global_stylesheet(theme_name),
        'theme': THEMES[theme_name]
    }

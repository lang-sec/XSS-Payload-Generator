"""
主题配置模块 - 支持浅色/暗夜模式切换
"""

# ============ 浅色主题 ============
LIGHT = {
    'bg': '#F8F9FA',          # 主背景
    'panel': '#FFFFFF',        # 卡片/面板背景
    'border': '#DCDFE6',       # 主边框
    'border2': '#D1D5DB',      # 按钮边框
    'border_light': '#E5E7EB', # 浅边框
    'text': '#303133',         # 主文字
    'text2': '#606266',        # 次要文字
    'text3': '#909399',        # 提示文字
    'accent': '#374151',       # 强调色
    'accent_hover': '#9CA3AF', # 悬停边框
    'btn_bg': '#FFFFFF',       # 按钮背景
    'btn_pressed': '#FAFAFA',  # 按钮按下
    'input_bg': '#FFFFFF',     # 输入框背景
    'sel_bg': '#E8F4F8',       # 选中背景
    'sel_text': '#1F2937',     # 选中文字
    'hover': '#F5F5F5',        # 悬停背景
    'list_hover': '#ecf5ff',   # 列表悬停
    'tab_bg': '#f5f7fa',       # 标签背景
    'code_bg': '#f5f7fa',      # 代码块背景
    'header_bg': '#FFFFFF',    # 顶栏背景
    'status_bg': '#f0f9ff',    # 状态标签背景
    'warning_bg': '#FEF0F0',   # 警告背景
    'warning_text': '#F56C6C', # 警告文字
    'warning_border': '#FBC4C4', # 警告边框
}

# ============ 暗夜主题 ============
DARK = {
    'bg': '#1C1C1C',           # 主背景（纯中性深灰）
    'panel': '#262626',        # 卡片/面板背景（高一档）
    'border': '#383838',       # 主边框
    'border2': '#4A4A4A',      # 按钮/控件边框（可见）
    'border_light': '#2E2E2E', # 浅边框/分隔
    'text': '#E4E4E4',         # 主文字（柔和近白）
    'text2': '#A0A0A0',        # 次要文字（中灰）
    'text3': '#707070',        # 提示文字（深灰）
    'accent': '#C2C2C2',       # 强调色（中性浅灰，全局统一）
    'accent_hover': '#DADADA', # 悬停（更亮的中性灰）
    'btn_bg': '#2D2D2D',       # 按钮背景（与 panel 同族）
    'btn_pressed': '#363636',  # 按钮按下
    'input_bg': '#202020',     # 输入框背景（略深，凹陷感）
    'sel_bg': '#3A3A3A',       # 选中背景（中性灰，提亮）
    'sel_text': '#FFFFFF',     # 选中文字
    'hover': '#2D2D2D',        # 悬停背景
    'list_hover': '#2F2F2F',   # 列表悬停
    'tab_bg': '#202020',       # 标签背景
    'code_bg': '#202020',      # 代码块背景（与 bg 区分）
    'header_bg': '#202020',    # 顶栏背景
    'status_bg': '#3A3A3A',    # 状态标签背景（中性灰）
    'warning_bg': '#3A2826',   # 警告背景（暗红，中性暖调）
    'warning_text': '#EFA593', # 警告文字（柔和橙红）
    'warning_border': '#4E3531', # 警告边框
}

THEMES = {'light': LIGHT, 'dark': DARK}


def get_global_stylesheet(theme_name='light'):
    """生成全局样式表"""
    t = THEMES[theme_name]

    return f"""
        QMainWindow {{
            background: {t['bg']};
        }}
        QWidget {{
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            font-size: 13px;
        }}
        QTabWidget::pane {{
            border: none;
            background: {t['panel']};
        }}
        QTabBar::tab {{
            background: {t['tab_bg']};
            color: {t['text2']};
            padding: 10px 20px;
            margin-right: 2px;
            border: none;
            border-bottom: 2px solid transparent;
            font-size: 13px;
            min-width: 100px;
        }}
        QTabBar::tab:selected {{
            color: {t['text']};
            border-bottom: 2px solid {t['accent']};
            background: {t['panel']};
            font-weight: 400;
        }}
        QTabBar::tab:hover {{
            color: {t['text']};
        }}
        QGroupBox {{
            border: 1px solid {t['border']};
            border-radius: 4px;
            margin-top: 10px;
            padding: 15px;
            background: {t['panel']};
            font-weight: 400;
            font-size: 13px;
        }}
        QGroupBox::title {{
            color: {t['text']};
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            font-weight: 400;
            font-size: 13px;
        }}
        QLineEdit, QComboBox {{
            border: 1px solid {t['border']};
            border-radius: 4px;
            padding: 8px 12px;
            background: {t['input_bg']};
            color: {t['text2']};
            font-size: 13px;
        }}
        QLineEdit:focus, QComboBox:focus {{
            border-color: {t['accent']};
        }}
        QSpinBox {{
            border: 1px solid {t['border']};
            border-radius: 4px;
            padding: 8px 12px;
            background: {t['input_bg']};
            color: {t['text2']};
            font-size: 13px;
        }}
        QSpinBox:focus {{
            border-color: {t['accent']};
        }}
        QSpinBox::up-button, QSpinBox::down-button {{
            background: {t['btn_bg']};
            border: 1px solid {t['border']};
            border-radius: 2px;
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background: {t['hover']};
        }}
        QPushButton {{
            background: {t['btn_bg']};
            color: {t['accent']};
            border: 1px solid {t['border2']};
            border-radius: 6px;
            padding: 9px 15px;
            font-size: 13px;
            font-weight: 400;
            font-family: "Microsoft YaHei";
        }}
        QPushButton:hover {{
            background: {t['btn_bg']};
            border-color: {t['accent_hover']};
        }}
        QPushButton:pressed {{
            background: {t['btn_pressed']};
        }}
        QTextEdit {{
            border: 1px solid {t['border']};
            border-radius: 4px;
            padding: 10px;
            background: {t['input_bg']};
            font-family: "Consolas", "Courier New", monospace;
            color: {t['text']};
            font-size: 13px;
            line-height: 1.5;
        }}
        QCheckBox {{
            color: {t['text']};
            spacing: 10px;
            font-size: 13px;
        }}
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {t['border2']};
            border-radius: 4px;
            background: {t['panel']};
        }}
        QCheckBox::indicator:hover {{
            border-color: {t['accent_hover']};
            background: {t['panel']};
        }}
        QCheckBox::indicator:checked {{
            background: {t['accent']};
            border-color: {t['accent']};
        }}
        QListWidget {{
            border: 1px solid {t['border']};
            border-radius: 4px;
            background: {t['panel']};
            font-size: 13px;
            outline: none;
            color: {t['text']};
        }}
        QListWidget::item {{
            padding: 8px;
            border-radius: 3px;
            outline: none;
            color: {t['text']};
        }}
        QListWidget::item:selected {{
            background: {t['sel_bg']};
            color: {t['sel_text']};
            outline: none;
            font-weight: 500;
        }}
        QListWidget::item:hover {{
            background: {t['list_hover']};
            color: {t['text']};
        }}
        QListWidget::item:focus {{
            outline: none;
        }}
        QLabel {{
            color: {t['text2']};
            font-size: 13px;
        }}
        QLabel#statusLabel {{
            color: {t['text']};
            padding: 8px 12px;
            background: {t['status_bg']};
            border-radius: 4px;
        }}
        QTableWidget {{
            border: 1px solid {t['border']};
            border-radius: 4px;
            background: {t['panel']};
            gridline-color: {t['border']};
            outline: none;
        }}
        QTableWidget::item {{
            padding: 10px;
            border-bottom: 1px solid {t['border']};
            outline: none;
            color: {t['text2']};
        }}
        QTableWidget::item:selected {{
            background: {t['sel_bg']};
            color: {t['sel_text']};
            outline: none;
        }}
        QTableWidget::item:focus {{
            outline: none;
            border: none;
        }}
        QHeaderView::section {{
            background: {t['code_bg']};
            padding: 12px;
            border: none;
            border-bottom: 2px solid {t['border']};
            font-weight: 400;
            color: {t['text']};
            font-size: 13px;
            outline: none;
        }}
        QHeaderView {{
            background: {t['code_bg']};
        }}
        QTableWidget QTableCornerButton::section {{
            background: {t['code_bg']};
            border: none;
        }}
        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 30px 2px 30px 2px;
        }}
        QScrollBar::handle:vertical {{
            background: {t['border']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {t['text2']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
            background: none;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
            margin: 2px 30px 2px 30px;
        }}
        QScrollBar::handle:horizontal {{
            background: {t['border']};
            border-radius: 4px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {t['text2']};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
            background: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}
        QMenu {{
            background: {t['panel']};
            border: 1px solid {t['border']};
            border-radius: 4px;
            padding: 5px;
            color: {t['text2']};
        }}
        QMenu::item {{
            padding: 8px 20px;
            border-radius: 3px;
        }}
        QMenu::item:selected {{
            background: {t['hover']};
            color: {t['text']};
        }}
    """


def get_inline_styles(theme_name='light'):
    """生成所有内联样式的字典 - 供组件使用"""
    t = THEMES[theme_name]

    return {
        'label_primary': f"font-weight: 400; font-size: 13px; color: {t['text']};",
        'label_secondary': f"color: {t['text2']}; padding: 5px;",
        'label_hint': f"color: {t['text3']}; font-size: 13px;",
        'label_title': f"font-size: 18px; font-weight: 400; color: {t['text']};",
        'label_subtitle': f"font-size: 13px; font-weight: 400; color: {t['text']};",
        'result_label': f"font-weight: 400; font-size: 13px; color: {t['text']}; padding: 10px 0 5px 0;",
        'context_result': f"padding: 15px; background: {t['code_bg']}; border-radius: 4px;",
        'button_primary': f"background: {t['btn_bg']}; color: {t['accent']}; border: 1px solid {t['border2']}; border-radius: 6px; padding: 10px; font-weight: 400; font-size: 13px;",
        'button_small': f"background: {t['btn_bg']}; color: {t['accent']}; border: 1px solid {t['border2']}; border-radius: 6px; padding: 6px 15px; font-weight: 400; font-size: 13px;",
        'button_add': f"background: {t['btn_bg']}; color: {t['accent']}; border: 1px solid {t['border2']}; border-radius: 6px; padding: 8px 20px; font-weight: 400; font-size: 13px;",
        'divider': f"background: {t['border']};",
        'count_label': f"font-weight: 400; color: {t['text2']}; font-size: 13px;",
        'count_hint': f"color: {t['text3']}; font-size: 13px;",
        'tip_text': f"color: {t['text3']}; font-size: 12px; padding: 0; margin-bottom: 10px;",
        'info_text': f"color: {t['text2']}; padding: 10px; font-size: 13px;",
        'warning_label': f"background: {t['warning_bg']}; color: {t['warning_text']}; padding: 10px; border-radius: 4px; border: 1px solid {t['warning_border']};",
    }


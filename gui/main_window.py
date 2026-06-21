"""
主窗口模块 - 整合所有标签页
"""
import sys
from gui import *
from gui.generator_tab import GeneratorTab
from gui.filter_tab import FilterTab
from gui.context_tab import ContextTab
from gui.mutator_tab import MutatorTab
from gui.preview_tab import PreviewTab
from gui.custom_tab import CustomTab
from gui.history_tab import HistoryTab
from gui.knowledge_tab import KnowledgeTab
from core.payload_manager import PayloadManager


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.payload_manager = PayloadManager()
        self.current_theme = 'light'
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle('XSS生成器')
        self.setGeometry(100, 100, 1400, 800)

        # 应用初始主题
        self.apply_theme()

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部标题栏
        header = self.create_header()
        main_layout.addWidget(header)

        # 标签页
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        # 页面1: 生成器
        self.tab_generator = GeneratorTab(self)
        self.tabs.addTab(self.tab_generator, "Payload生成器")

        # 页面2: 筛选器
        self.tab_filter = FilterTab(self)
        self.tabs.addTab(self.tab_filter, "Payload筛选")

        # 页面3: 上下文适配
        self.tab_context = ContextTab(self)
        self.tabs.addTab(self.tab_context, "上下文适配")

        # 页面4: 变异器
        self.tab_mutator = MutatorTab(self)
        self.tabs.addTab(self.tab_mutator, "Payload变异器")

        # 页面5: 效果预览
        self.tab_preview = PreviewTab(self)
        self.tabs.addTab(self.tab_preview, "效果预览")

        # 页面6: 历史记录
        self.tab_history = HistoryTab(self)
        self.tabs.addTab(self.tab_history, "历史记录")

        # 页面7: 知识库
        self.tab_knowledge = KnowledgeTab(self)
        self.tabs.addTab(self.tab_knowledge, "XSS知识库")

        # 页面8: 自定义Payload
        self.tab_custom = CustomTab(self)
        self.tabs.addTab(self.tab_custom, "自定义Payload")

        main_layout.addWidget(self.tabs)

        # 底部状态栏
        self.statusBar().showMessage('就绪')

    def create_header(self):
        """创建顶部标题栏 - 专业设计 + SVG图标"""
        self.header = QWidget()
        self.header.setFixedHeight(64)

        layout = QHBoxLayout(self.header)
        layout.setContentsMargins(24, 0, 24, 0)

        # 左侧：应用名称
        left_layout = QHBoxLayout()
        left_layout.setSpacing(12)

        self.header_title = QLabel("XSS Payload Generator")
        self.header_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 400;
            letter-spacing: -0.5px;
            font-family: "LXGW WenKai", "霞鹜文楷", "Microsoft YaHei";
        """)
        left_layout.addWidget(self.header_title)

        layout.addLayout(left_layout)
        layout.addStretch()

        # 右侧：主题切换按钮
        self.theme_btn = QPushButton("暗夜模式")
        self.theme_btn.setStyleSheet("padding: 6px 12px; font-size: 13px;")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)

        return self.header

    def apply_theme(self):
        """应用主题"""
        # 应用全局样式表
        self.setStyleSheet(get_global_stylesheet(self.current_theme))

        # 获取主题颜色
        t = THEMES[self.current_theme]

        # 更新顶栏样式
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                QWidget {{
                    background: {t['header_bg']};
                    border-bottom: 1px solid {t['border_light']};
                }}
            """)

            # 更新标题颜色
            if hasattr(self, 'header_title'):
                self.header_title.setStyleSheet(f"""
                    font-size: 18px;
                    font-weight: 400;
                    color: {t['text']};
                    letter-spacing: -0.5px;
                    font-family: "LXGW WenKai", "霞鹜文楷", "Microsoft YaHei";
                """)

        # 更新各标签页的内联样式
        self.update_tab_styles(t)

        # 更新知识库内容
        if hasattr(self, 'tab_knowledge'):
            self.tab_knowledge.update_knowledge_content()

    def update_tab_styles(self, t):
        """更新所有标签页的内联样式"""
        # 更新生成器标签页
        if hasattr(self, 'tab_generator'):
            if hasattr(self.tab_generator, 'cat_label'):
                self.tab_generator.cat_label.setStyleSheet(f"font-weight: 400; font-size: 13px; color: {t['text']};")
            if hasattr(self.tab_generator, 'payload_label'):
                self.tab_generator.payload_label.setStyleSheet(f"font-weight: 400; font-size: 13px; color: {t['text']};")
            if hasattr(self.tab_generator, 'length_label'):
                self.tab_generator.length_label.setStyleSheet(f"color: {t['text2']}; padding: 5px;")

        # 更新筛选器标签页
        if hasattr(self, 'tab_filter'):
            if hasattr(self.tab_filter, 'filter_result_label'):
                self.tab_filter.filter_result_label.setStyleSheet(f"font-weight: 400; font-size: 13px; color: {t['text']}; padding: 10px 0 5px 0;")

        # 更新上下文适配标签页
        if hasattr(self, 'tab_context'):
            if hasattr(self.tab_context, 'context_info'):
                self.tab_context.context_info.setStyleSheet(f"color: {t['text2']}; padding: 10px; font-size: 13px;")
            if hasattr(self.tab_context, 'context_result'):
                self.tab_context.context_result.setStyleSheet(f"padding: 15px; background: {t['input_bg']}; border-radius: 4px;")

        # 更新变异器标签页
        if hasattr(self, 'tab_mutator'):
            if hasattr(self.tab_mutator, 'mutate_title'):
                self.tab_mutator.mutate_title.setStyleSheet(f"font-size: 13px; font-weight: 400; color: {t['text']};")
            if hasattr(self.tab_mutator, 'mutate_result_title'):
                self.tab_mutator.mutate_result_title.setStyleSheet(f"font-weight: 400; font-size: 13px; color: {t['text']};")
            if hasattr(self.tab_mutator, 'mutate_count_label'):
                self.tab_mutator.mutate_count_label.setStyleSheet(f"color: {t['text2']}; font-size: 13px;")

        # 更新预览标签页
        if hasattr(self, 'tab_preview'):
            if hasattr(self.tab_preview, 'preview_info'):
                self.tab_preview.preview_info.setStyleSheet(f"""
                    color: {t['text3']};
                    font-size: 13px;
                    padding: 2px 0;
                    line-height: 1.6;
                """)

    def toggle_theme(self):
        """切换主题"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

        # 更新主题切换按钮文字
        if self.current_theme == 'light':
            self.theme_btn.setText("暗夜模式")
        else:
            self.theme_btn.setText("浅色模式")

        self.statusBar().showMessage(
            f"已切换到{'暗夜' if self.current_theme == 'dark' else '浅色'}模式",
            2000
        )

    def add_to_history(self, category, payload):
        """添加到历史记录"""
        if hasattr(self, 'tab_history'):
            self.tab_history.add_history(category, payload)


def main():
    """主函数"""
    # 启用高DPI支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # 设置全局字体
    font = QFont("LXGW WenKai", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

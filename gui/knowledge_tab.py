"""
XSS知识库标签页
"""
from gui import *


class KnowledgeTab(QWidget):
    """XSS知识库标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QLabel("XSS知识库")
        title.setStyleSheet("font-size: 18px; font-weight: 400; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # 知识库内容
        self.knowledge_browser = QTextBrowser()
        self.knowledge_browser.setOpenExternalLinks(True)
        self.knowledge_browser.setFocusPolicy(Qt.NoFocus)

        # 加载初始内容
        self.update_knowledge_content()

        main_layout.addWidget(self.knowledge_browser)

    def update_knowledge_content(self):
        """更新知识库内容"""
        if self.parent_window:
            theme = self.parent_window.current_theme
            html_content = get_knowledge_html(theme)
            self.knowledge_browser.setHtml(html_content)

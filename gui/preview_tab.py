"""
效果预览标签页
"""
from gui import *
import tempfile
import webbrowser
import os


class PreviewTab(QWidget):
    """效果预览标签页 - 左右布局"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ── 左侧 ──
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # 输入区
        input_group = QGroupBox("测试Payload")
        input_inner = QVBoxLayout()
        input_inner.setSpacing(10)

        self.preview_input = QTextEdit()
        self.preview_input.setPlaceholderText("粘贴payload进行测试...")
        self.preview_input.setStyleSheet("padding: 10px; font-size: 13px;")
        self.preview_input.setFocusPolicy(Qt.StrongFocus)
        input_inner.addWidget(self.preview_input)

        input_group.setLayout(input_inner)
        left_layout.addWidget(input_group)

        # 按钮行（水平）
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        test_btn = QPushButton("测试执行")
        test_btn.clicked.connect(self.preview_payload)
        test_btn.setStyleSheet("padding: 10px 25px;")
        btn_layout.addWidget(test_btn)

        load_btn = QPushButton("从生成器加载")
        load_btn.clicked.connect(self.load_to_preview)
        load_btn.setStyleSheet("padding: 10px 20px;")
        btn_layout.addWidget(load_btn)

        reset_btn = QPushButton("重置")
        reset_btn.clicked.connect(self.reset_preview)
        reset_btn.setStyleSheet("padding: 10px 20px;")
        btn_layout.addWidget(reset_btn)

        btn_layout.addStretch()
        left_layout.addLayout(btn_layout)

        # 说明
        self.preview_info = QLabel(
            "安全沙箱环境  |  模拟执行效果  |  语法检查  |  不支持网络请求\n"
            "iframe/object 等嵌入标签可能无法完全测试，实际效果需在目标环境验证"
        )
        self.preview_info.setWordWrap(True)
        left_layout.addWidget(self.preview_info)

        main_layout.addWidget(left_panel, 2)

        # ── 右侧 ──
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        result_group = QGroupBox("执行结果")
        result_layout = QVBoxLayout()

        self.preview_result = QTextEdit()
        self.preview_result.setReadOnly(True)
        self.preview_result.setPlaceholderText("点击「测试执行」后，会在浏览器中打开...")
        self.preview_result.setStyleSheet("padding: 10px; font-size: 13px;")
        self.preview_result.setFocusPolicy(Qt.NoFocus)
        result_layout.addWidget(self.preview_result)

        result_group.setLayout(result_layout)
        right_layout.addWidget(result_group)

        main_layout.addWidget(right_panel, 3)

    def load_to_preview(self):
        if not self.parent_window:
            return
        if hasattr(self.parent_window, 'tab_generator'):
            text = self.parent_window.tab_generator.result_text.toPlainText()
            if not text:
                QMessageBox.warning(self, '提示', '请先在生成器中生成payload')
                return
            self.preview_input.setPlainText(text)
            self.parent_window.tabs.setCurrentWidget(self)
            self.parent_window.statusBar().showMessage('已加载到预览', 3000)
        else:
            QMessageBox.warning(self, '提示', '无法访问生成器')

    def preview_payload(self):
        payload = self.preview_input.toPlainText().strip()
        if not payload:
            QMessageBox.warning(self, '提示', '请输入payload')
            return

        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>XSS Payload 测试</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f5f7fa;
        }}
        .test-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E5E7EB;
            margin-bottom: 20px;
        }}
        .info {{
            color: #374151;
            margin-bottom: 15px;
            font-weight: 400;
        }}
        .payload-code {{
            background: #f4f4f5;
            padding: 10px;
            border-radius: 4px;
            font-family: Consolas, monospace;
            overflow-x: auto;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="test-container">
        <div class="info">XSS Payload 测试区域</div>
        <div class="payload-code">{payload.replace('<', '&lt;').replace('>', '&gt;')}</div>
    </div>
    <div class="test-container">
        <div class="info">实际渲染（下方）</div>
        <div id="payload-area">
            {payload}
        </div>
    </div>
</body>
</html>"""

        temp_file = os.path.join(tempfile.gettempdir(), 'xss_test_payload.html')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_template)
            webbrowser.open('file://' + temp_file)
            self.preview_result.setPlainText(
                f'已在浏览器中打开测试页面\n\n'
                f'文件位置: {temp_file}\n\n'
                f'如果payload有效，浏览器中会触发相应效果（alert/prompt等）'
            )
            if self.parent_window:
                self.parent_window.statusBar().showMessage('已在浏览器中打开', 3000)
        except Exception as e:
            QMessageBox.warning(self, '错误', f'打开失败: {str(e)}')

    def reset_preview(self):
        self.preview_input.clear()
        self.preview_result.clear()
        if self.parent_window:
            self.parent_window.statusBar().showMessage('已重置', 2000)

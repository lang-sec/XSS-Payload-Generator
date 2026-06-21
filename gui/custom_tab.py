"""
自定义Payload标签页
"""
from gui import *


class CustomTab(QWidget):
    """自定义Payload标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        self.load_custom_payloads()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题和说明
        header_layout = QHBoxLayout()
        title = QLabel("自定义Payload管理")
        title.setStyleSheet("font-size: 18px; font-weight: 400;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        add_btn = QPushButton("添加新Payload")
        add_btn.clicked.connect(self.add_custom_payload)
        header_layout.addWidget(add_btn)

        main_layout.addLayout(header_layout)

        desc = QLabel("管理你自己收集的Payload，双击单元格可复制内容")
        desc.setStyleSheet("color: #909399; margin-bottom: 10px;")
        main_layout.addWidget(desc)

        # Payload列表（表格形式）
        self.custom_payload_table = QTableWidget()
        self.custom_payload_table.setColumnCount(3)
        self.custom_payload_table.setHorizontalHeaderLabels(["名称", "来源", "Payload代码"])
        self.custom_payload_table.horizontalHeader().setStretchLastSection(True)
        self.custom_payload_table.setSelectionBehavior(QTableWidget.SelectItems)
        self.custom_payload_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.custom_payload_table.setAlternatingRowColors(False)
        self.custom_payload_table.itemDoubleClicked.connect(self.copy_cell_on_double_click)
        self.custom_payload_table.setFocusPolicy(Qt.NoFocus)
        self.custom_payload_table.verticalHeader().setDefaultSectionSize(40)
        self.custom_payload_table.verticalHeader().setMinimumSectionSize(35)

        # 设置列宽
        self.custom_payload_table.setColumnWidth(0, 200)
        self.custom_payload_table.setColumnWidth(1, 150)

        # 右键菜单
        self.custom_payload_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.custom_payload_table.customContextMenuRequested.connect(self.show_context_menu)

        main_layout.addWidget(self.custom_payload_table)

    def load_custom_payloads(self):
        """加载自定义payload"""
        if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
            payloads = self.parent_window.payload_manager.get_custom_payloads()
            self.update_table(payloads)

    def update_table(self, payloads):
        """更新表格显示"""
        self.custom_payload_table.setRowCount(len(payloads))

        for i, payload in enumerate(payloads):
            self.custom_payload_table.setItem(i, 0, QTableWidgetItem(payload.get('name', '')))
            self.custom_payload_table.setItem(i, 1, QTableWidgetItem(payload.get('source', '')))
            # 兼容code和payload两种字段名
            code = payload.get('payload') or payload.get('code', '')
            self.custom_payload_table.setItem(i, 2, QTableWidgetItem(code))

    def add_custom_payload(self):
        """添加自定义payload"""
        dialog = QDialog(self)
        dialog.setWindowTitle("添加自定义Payload")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout(dialog)

        # 名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("名称:"))
        name_input = QLineEdit()
        name_input.setPlaceholderText("例如: 我的XSS Payload")
        name_layout.addWidget(name_input)
        layout.addLayout(name_layout)

        # 来源
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("来源:"))
        source_input = QLineEdit()
        source_input.setPlaceholderText("例如: HackerOne, 实战, 自己研究")
        source_layout.addWidget(source_input)
        layout.addLayout(source_layout)

        # Payload
        layout.addWidget(QLabel("Payload代码:"))
        payload_input = QTextEdit()
        payload_input.setPlaceholderText("粘贴你的Payload代码...")
        payload_input.setMaximumHeight(150)
        layout.addWidget(payload_input)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(lambda: self.save_custom_payload(
            dialog, name_input.text(), source_input.text(), payload_input.toPlainText()
        ))
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)

        dialog.exec_()

    def save_custom_payload(self, dialog, name, source, payload):
        """保存自定义payload"""
        if not name or not payload:
            QMessageBox.warning(self, "警告", "名称和Payload不能为空！")
            return

        if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
            success = self.parent_window.payload_manager.add_custom_payload(name, source, payload)
            if success:
                self.load_custom_payloads()
                dialog.accept()
                self.parent_window.statusBar().showMessage('Payload已添加', 2000)
            else:
                QMessageBox.critical(self, "错误", "保存失败！")

    def copy_cell_on_double_click(self, item):
        """双击单元格复制内容"""
        text = item.text()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            if self.parent_window:
                self.parent_window.statusBar().showMessage('已复制', 2000)

    def show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.custom_payload_table.itemAt(pos)
        if item:
            menu = QMenu(self)
            copy_action = menu.addAction("复制")
            delete_action = menu.addAction("删除")

            action = menu.exec_(self.custom_payload_table.mapToGlobal(pos))

            if action == copy_action:
                self.copy_cell_on_double_click(item)
            elif action == delete_action:
                self.delete_payload(item.row())

    def delete_payload(self, row):
        """删除payload"""
        reply = QMessageBox.question(
            self,
            '确认删除',
            '确定要删除这个Payload吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.parent_window and hasattr(self.parent_window, 'payload_manager'):
                success = self.parent_window.payload_manager.delete_custom_payload(row)
                if success:
                    self.load_custom_payloads()
                    self.parent_window.statusBar().showMessage('已删除', 2000)

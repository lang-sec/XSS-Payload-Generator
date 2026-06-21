"""
历史记录标签页
"""
from gui import *
import json
import os
from datetime import datetime


class HistoryTab(QWidget):
    """历史记录标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.history_file = 'xss_history.json'
        self.history = []
        self.init_ui()
        self.load_history()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题和操作按钮
        header_layout = QHBoxLayout()
        title = QLabel("历史记录")
        title.setStyleSheet("font-size: 18px; font-weight: 400;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        clear_btn = QPushButton("清空历史")
        clear_btn.clicked.connect(self.clear_history)
        header_layout.addWidget(clear_btn)

        main_layout.addLayout(header_layout)

        # 历史记录表格
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["时间", "类型", "长度", "Payload"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setAlternatingRowColors(False)
        self.history_table.itemDoubleClicked.connect(self.load_from_history_double_click)
        self.history_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_history_context_menu)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.verticalHeader().setDefaultSectionSize(45)

        # 设置列宽
        self.history_table.setColumnWidth(0, 180)
        self.history_table.setColumnWidth(1, 180)
        self.history_table.setColumnWidth(2, 80)

        main_layout.addWidget(self.history_table)

    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                self.update_history_table()
        except Exception as e:
            print(f"加载历史记录失败: {e}")

    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def add_history(self, category, payload):
        """添加历史记录"""
        record = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'payload': payload
        }
        self.history.insert(0, record)

        # 限制历史记录数量
        if len(self.history) > 100:
            self.history = self.history[:100]

        self.save_history()
        self.update_history_table()

    def update_history_table(self):
        """更新历史记录表格"""
        self.history_table.setRowCount(len(self.history))

        for i, record in enumerate(self.history):
            self.history_table.setItem(i, 0, QTableWidgetItem(record['time']))
            self.history_table.setItem(i, 1, QTableWidgetItem(record['category']))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(len(record['payload']))))
            self.history_table.setItem(i, 3, QTableWidgetItem(record['payload']))

    def clear_history(self):
        """清空历史记录"""
        reply = QMessageBox.question(
            self,
            '确认清空',
            '确定要清空所有历史记录吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.history = []
            self.save_history()
            self.update_history_table()
            if self.parent_window:
                self.parent_window.statusBar().showMessage('历史记录已清空', 2000)

    def load_from_history_double_click(self, item):
        """双击历史记录项复制"""
        row = item.row()
        if 0 <= row < len(self.history):
            payload = self.history[row]['payload']
            clipboard = QApplication.clipboard()
            clipboard.setText(payload)
            if self.parent_window:
                self.parent_window.statusBar().showMessage('已复制历史记录', 2000)

    def show_history_context_menu(self, pos):
        """显示右键菜单"""
        item = self.history_table.itemAt(pos)
        if item:
            menu = QMenu(self)
            copy_action = menu.addAction("复制")
            delete_action = menu.addAction("删除")

            action = menu.exec_(self.history_table.mapToGlobal(pos))

            if action == copy_action:
                self.load_from_history_double_click(item)
            elif action == delete_action:
                row = item.row()
                if 0 <= row < len(self.history):
                    self.history.pop(row)
                    self.save_history()
                    self.update_history_table()

"""
Payload筛选器标签页 - 完全按照原版实现
"""
from gui import *
import re


class FilterTab(QWidget):
    """Payload筛选器：字符过滤 + 长度限制"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 上下布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 筛选条件（紧凑单行布局）
        condition_group = QGroupBox("根据规则筛选可用Payload")
        condition_layout = QVBoxLayout()
        condition_layout.setSpacing(10)

        # 第一行：长度限制 + 快捷规则
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("最大长度:"))
        self.length_input = QSpinBox()
        self.length_input.setRange(1, 1000)
        self.length_input.setValue(100)
        self.length_input.setSuffix(" 字符")
        row1.addWidget(self.length_input, 1)

        row1.addWidget(QLabel("快捷过滤:"))
        self.filter_presets = {
            "严格过滤": ["<", ">", "(", ")", "script", "on", "'", '"'],
            "标签过滤": ["<", ">", "script"],
            "事件过滤": ["on", "(", ")"],
            "引号过滤": ["'", '"'],
        }
        preset_combo = QComboBox()
        preset_combo.addItems(["不使用"] + list(self.filter_presets.keys()))
        preset_combo.currentTextChanged.connect(self.load_filter_preset)
        row1.addWidget(preset_combo, 2)
        condition_layout.addLayout(row1)

        # 第二行：自定义过滤
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("过滤字符:"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("逗号分隔，如: <,>,script,on")
        self.filter_input.setStyleSheet("padding: 8px;")
        row2.addWidget(self.filter_input, 1)

        search_btn = QPushButton("搜索可用Payload")
        search_btn.clicked.connect(self.search_payloads)
        search_btn.setStyleSheet("padding: 8px 20px; font-weight: 400; font-size: 13px;")
        row2.addWidget(search_btn)
        condition_layout.addLayout(row2)

        condition_group.setLayout(condition_layout)
        main_layout.addWidget(condition_group)

        # 结果表格（去掉GroupBox，直接显示）
        self.filter_result_label = QLabel("符合条件的Payload")
        self.filter_result_label.setStyleSheet("font-weight: 400; font-size: 13px; color: #303133; padding: 10px 0 5px 0;")
        main_layout.addWidget(self.filter_result_label)

        self.filter_table = QTableWidget()
        self.filter_table.setColumnCount(4)
        self.filter_table.setHorizontalHeaderLabels(['Payload', '长度', '分类', '操作'])
        self.filter_table.horizontalHeader().setStretchLastSection(False)
        self.filter_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.filter_table.setColumnWidth(1, 80)
        self.filter_table.setColumnWidth(2, 120)
        self.filter_table.setColumnWidth(3, 100)
        self.filter_table.verticalHeader().setVisible(False)
        self.filter_table.verticalHeader().setDefaultSectionSize(40)
        self.filter_table.setAlternatingRowColors(False)
        self.filter_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.filter_table.customContextMenuRequested.connect(self.show_filter_context_menu)
        self.filter_table.setFocusPolicy(Qt.NoFocus)
        main_layout.addWidget(self.filter_table)

    def load_filter_preset(self, preset):
        """加载预设规则"""
        if preset == "不使用":
            self.filter_input.clear()
        elif preset in self.filter_presets:
            chars = self.filter_presets[preset]
            self.filter_input.setText(','.join(chars))

    def search_payloads(self):
        """搜索payload"""
        if not self.parent_window or not hasattr(self.parent_window, 'payload_manager'):
            return

        max_length = self.length_input.value()
        filter_text = self.filter_input.text().strip()
        filters = [f.strip() for f in filter_text.split(',') if f.strip()] if filter_text else []

        # 获取所有payload
        all_payloads = []
        categories = self.parent_window.payload_manager.get_all_categories()

        for cat in categories:
            payloads_dict = self.parent_window.payload_manager.get_payloads_by_category(cat)
            for name, payload in payloads_dict.items():
                # 检查长度
                if len(payload) > max_length:
                    continue

                # 检查过滤 - 忽略base64编码部分
                blocked = False
                if filters:
                    # 移除base64部分后再检测
                    check_payload = re.sub(r';base64,[A-Za-z0-9+/=]+', '', payload)
                    for f in filters:
                        if f.lower() in check_payload.lower():
                            blocked = True
                            break

                if not blocked:
                    all_payloads.append((payload, len(payload), cat, name))

        # 排序（按长度）
        all_payloads.sort(key=lambda x: x[1])

        # 显示结果
        self.filter_table.setRowCount(0)
        for i, (payload, length, cat, name) in enumerate(all_payloads):
            self.filter_table.insertRow(i)

            # Payload
            self.filter_table.setItem(i, 0, QTableWidgetItem(payload))

            # 长度
            length_item = QTableWidgetItem(str(length))
            length_item.setTextAlignment(Qt.AlignCenter)
            self.filter_table.setItem(i, 1, length_item)

            # 分类
            self.filter_table.setItem(i, 2, QTableWidgetItem(cat))

            # 复制按钮
            copy_btn = QPushButton("复制")
            copy_btn.setStyleSheet("padding: 5px 10px; min-height: 28px;")
            copy_btn.clicked.connect(lambda checked, p=payload: self.copy_filter_payload(p))
            self.filter_table.setCellWidget(i, 3, copy_btn)

        self.filter_table.resizeRowsToContents()

        filter_desc = f"过滤: {', '.join(filters)}" if filters else "无过滤"
        if self.parent_window:
            self.parent_window.statusBar().showMessage(
                f'找到{len(all_payloads)}个payload (长度≤{max_length}, {filter_desc})',
                5000
            )

    def copy_filter_payload(self, payload):
        """复制payload"""
        QApplication.clipboard().setText(payload)
        if self.parent_window:
            self.parent_window.statusBar().showMessage('已复制', 2000)

    def show_filter_context_menu(self, position):
        """显示筛选表格右键菜单"""
        current_row = self.filter_table.currentRow()
        if current_row < 0:
            return

        # 获取当前行的payload
        payload_item = self.filter_table.item(current_row, 0)
        if not payload_item:
            return

        payload = payload_item.text()

        menu = QMenu(self)
        copy_action = menu.addAction("复制")

        action = menu.exec_(self.filter_table.mapToGlobal(position))

        if action == copy_action:
            self.copy_filter_payload(payload)

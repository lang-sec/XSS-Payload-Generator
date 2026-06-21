"""
Payload变异器标签页 - 完全按照原版实现
"""
from gui import *
import re


class MutatorTab(QWidget):
    """变异器标签页 - 左右布局增强版"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 左右布局"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧：输入和选项
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # 标题
        self.mutate_title = QLabel("Payload变异器")
        self.mutate_title.setStyleSheet("font-size: 13px; font-weight: 400; color: #303133;")
        left_layout.addWidget(self.mutate_title)

        # 输入区域
        input_group = QGroupBox("输入原始Payload")
        input_layout = QVBoxLayout()
        self.mutate_input = QTextEdit()
        self.mutate_input.setPlaceholderText("粘贴或输入payload\n例如: <img src=x onerror=alert(1)>")
        self.mutate_input.setMaximumHeight(120)
        self.mutate_input.setFocusPolicy(Qt.StrongFocus)
        input_layout.addWidget(self.mutate_input)
        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)

        # 变异选项
        options_group = QGroupBox("变异选项")
        options_layout = QVBoxLayout()
        options_layout.setSpacing(8)

        self.mutate_space = CustomCheckBox("空格变换 (/, \\n, \\t, /**/)")
        self.mutate_space.setChecked(True)
        options_layout.addWidget(self.mutate_space)

        self.mutate_quote = CustomCheckBox("引号变换 (', \", `)")
        self.mutate_quote.setChecked(True)
        options_layout.addWidget(self.mutate_quote)

        self.mutate_case = CustomCheckBox("大小写混淆 (ImG, OnErRoR)")
        self.mutate_case.setChecked(True)
        options_layout.addWidget(self.mutate_case)

        self.mutate_encode = CustomCheckBox("编码变换 (HTML实体, Unicode, Hex)")
        self.mutate_encode.setChecked(True)
        options_layout.addWidget(self.mutate_encode)

        self.mutate_comment = CustomCheckBox("注释插入 (</**/img/**/>)")
        self.mutate_comment.setChecked(True)
        options_layout.addWidget(self.mutate_comment)

        self.mutate_tag = CustomCheckBox("标签替换 (img→svg)")
        self.mutate_tag.setChecked(True)
        options_layout.addWidget(self.mutate_tag)

        self.mutate_attribute = CustomCheckBox("属性变换 (src=x→src=1)")
        self.mutate_attribute.setChecked(True)
        options_layout.addWidget(self.mutate_attribute)

        self.mutate_obfuscate = CustomCheckBox("深度混淆 (fromCharCode, 拼接)")
        self.mutate_obfuscate.setChecked(False)
        options_layout.addWidget(self.mutate_obfuscate)

        options_group.setLayout(options_layout)
        left_layout.addWidget(options_group)

        # 按钮
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)

        self.mutate_gen_btn = QPushButton("生成变种")
        self.mutate_gen_btn.clicked.connect(self.do_mutate_enhanced)
        btn_layout.addWidget(self.mutate_gen_btn)

        copy_all_btn = QPushButton("复制全部")
        copy_all_btn.clicked.connect(self.copy_all_mutations)
        copy_all_btn.setStyleSheet("padding: 8px;")
        btn_layout.addWidget(copy_all_btn)

        export_btn = QPushButton("导出变种")
        export_btn.clicked.connect(self.export_mutations)
        export_btn.setStyleSheet("padding: 8px;")
        btn_layout.addWidget(export_btn)

        left_layout.addLayout(btn_layout)
        left_layout.addStretch()

        main_layout.addWidget(left_panel, 2)

        # 右侧：结果展示
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # 结果标题
        result_header = QHBoxLayout()
        self.mutate_result_title = QLabel("变异结果")
        self.mutate_result_title.setStyleSheet("font-weight: 400; font-size: 13px; color: #303133;")
        result_header.addWidget(self.mutate_result_title)

        self.mutate_count_label = QLabel("变种数量: 0")
        self.mutate_count_label.setStyleSheet("color: #909399; font-size: 13px;")
        result_header.addWidget(self.mutate_count_label)
        result_header.addStretch()

        right_layout.addLayout(result_header)

        # 结果文本框
        self.mutate_output = QTextEdit()
        self.mutate_output.setReadOnly(True)
        self.mutate_output.setPlaceholderText("点击\"生成变种\"按钮，将在此显示所有变异后的payload...")
        self.mutate_output.setFocusPolicy(Qt.NoFocus)
        right_layout.addWidget(self.mutate_output)

        main_layout.addWidget(right_panel, 3)

    def do_mutate_enhanced(self):
        """增强的变异生成"""
        payload = self.mutate_input.toPlainText().strip()
        if not payload:
            QMessageBox.warning(self, '提示', '请输入payload')
            return

        mutations = []
        seen = {payload}

        # 1. 空格变换
        if self.mutate_space.isChecked():
            mutations.append(("空格→斜杠", payload.replace(' ', '/')))
            mutations.append(("空格→换行", payload.replace(' ', '\n')))
            mutations.append(("空格→Tab", payload.replace(' ', '\t')))
            mutations.append(("空格→注释", payload.replace(' ', '/**/')))

        # 2. 引号变换
        if self.mutate_quote.isChecked() and ('"' in payload or "'" in payload):
            mutations.append(("双引号→单引号", payload.replace('"', "'")))
            mutations.append(("引号→反引号", payload.replace('"', '`').replace("'", '`')))
            if 'alert' in payload:
                mutations.append(("移除引号", payload.replace('"', '').replace("'", '')))

        # 3. 大小写混淆
        if self.mutate_case.isChecked():
            if '<' in payload and '>' in payload:
                mutations.append(("标签大小写", self._case_mutate_tags(payload)))
            if 'onerror' in payload:
                mutations.append(("onerror混淆", payload.replace('onerror', 'OnErRoR')))
            if 'onload' in payload:
                mutations.append(("onload混淆", payload.replace('onload', 'OnLoAd')))
            if 'alert' in payload.lower():
                mutations.append(("alert混淆", self._case_mutate_word(payload, 'alert')))

        # 4. 编码变换
        if self.mutate_encode.isChecked():
            if 'alert' in payload.lower():
                # HTML实体编码
                encoded = payload.replace('alert', '&#97;&#108;&#101;&#114;&#116;')
                mutations.append(("alert-HTML实体", encoded))

                # Unicode编码
                unicode_encoded = payload.replace('alert', '\\u0061\\u006c\\u0065\\u0072\\u0074')
                mutations.append(("alert-Unicode", unicode_encoded))

                # Hex编码
                hex_encoded = payload.replace('alert', '\\x61\\x6c\\x65\\x72\\x74')
                mutations.append(("alert-Hex", hex_encoded))

        # 5. 注释插入
        if self.mutate_comment.isChecked():
            if '<' in payload and '>' in payload:
                commented = payload.replace('<', '</**/').replace('>', '/**/>').replace('=', '/**/=/**/')
                mutations.append(("注释混淆", commented))

        # 6. 标签替换
        if self.mutate_tag.isChecked():
            if '<img' in payload:
                mutations.append(("img→svg", payload.replace('<img', '<svg').replace('onerror', 'onload')))
                mutations.append(("img→iframe", payload.replace('<img src=x onerror=', '<iframe onload=')))
            if '<script>' in payload:
                mutations.append(("script→svg", payload.replace('<script>', '<svg><script>').replace('</script>', '</script></svg>')))

        # 7. 属性变换
        if self.mutate_attribute.isChecked():
            if 'src=x' in payload:
                mutations.append(("src=x→src=1", payload.replace('src=x', 'src=1')))
                mutations.append(("添加多余属性", payload.replace('<img', '<img id=x class=y')))

        # 8. 深度混淆
        if self.mutate_obfuscate.isChecked():
            if 'alert' in payload.lower():
                # String.fromCharCode
                char_codes = ','.join(str(ord(c)) for c in 'alert(1)')
                obf1 = payload.replace('alert(1)', f'eval(String.fromCharCode({char_codes}))')
                mutations.append(("fromCharCode混淆", obf1))

                # 拼接混淆
                obf2 = payload.replace('alert(1)', "eval('ale'+'rt(1)')")
                mutations.append(("字符串拼接", obf2))

                # 方括号混淆
                obf3 = payload.replace('alert(1)', "window['alert'](1)")
                mutations.append(("方括号访问", obf3))

        # 去重并输出
        unique_mutations = []
        for name, mutated in mutations:
            if mutated != payload and mutated not in seen:
                seen.add(mutated)
                unique_mutations.append((name, mutated))

        if not unique_mutations:
            self.mutate_output.setPlainText('该payload在当前选项下没有可用的变异方式')
            self.mutate_count_label.setText("变种数量: 0")
            return

        output = [f"━━━━━ 原始Payload ━━━━━\n{payload}\n"]
        for i, (name, mutated) in enumerate(unique_mutations, 1):
            output.append(f"━━━━━ 变种{i}: {name} ━━━━━\n{mutated}\n")

        self.mutate_output.setPlainText('\n'.join(output))
        self.mutate_count_label.setText(f"变种数量: {len(unique_mutations)}")

        if self.parent_window:
            self.parent_window.statusBar().showMessage(f'生成了{len(unique_mutations)}个变种', 3000)

    def _case_mutate_tags(self, payload):
        """标签大小写混淆"""
        def mix_case(match):
            tag = match.group(0)
            return ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(tag))
        return re.sub(r'<[a-z]+', mix_case, payload, flags=re.IGNORECASE)

    def _case_mutate_word(self, payload, word):
        """单词大小写混淆"""
        mixed = ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(word))
        return re.sub(word, mixed, payload, flags=re.IGNORECASE)

    def copy_all_mutations(self):
        """复制所有变种"""
        text = self.mutate_output.toPlainText()
        if text and '原始Payload' in text:
            QApplication.clipboard().setText(text)
            if self.parent_window:
                self.parent_window.statusBar().showMessage('已复制所有变种', 3000)
        else:
            QMessageBox.warning(self, '提示', '请先生成变种')

    def export_mutations(self):
        """导出变种到文件"""
        text = self.mutate_output.toPlainText()
        if not text or '原始Payload' not in text:
            QMessageBox.warning(self, '提示', '请先生成变种')
            return

        filename, _ = QFileDialog.getSaveFileName(self, '导出变种', 'mutations.txt', 'Text Files (*.txt)')
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                if self.parent_window:
                    self.parent_window.statusBar().showMessage(f'已导出到: {filename}', 3000)
            except:
                QMessageBox.warning(self, '错误', '导出失败')

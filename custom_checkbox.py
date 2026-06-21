from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush

class CustomCheckBox(QCheckBox):
    """自定义打勾复选框 - 支持主题"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
                font-size: 13px;
            }
        """)

    def paintEvent(self, event):
        """自定义绘制"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 获取当前主题颜色
        bg_color = self.palette().color(QPalette.Base)
        text_color = self.palette().color(QPalette.Text)
        is_light_theme = bg_color.lightness() > 128

        # 复选框的位置和大小
        checkbox_rect = QRect(0, (self.height() - 18) // 2, 18, 18)

        if self.isChecked():
            # 选中状态：填充背景
            if is_light_theme:
                fill_color = QColor("#374151")
                check_color = QColor("#FFFFFF")
            else:
                fill_color = QColor("#C2C2C2")  # 中性浅灰（与强调色统一）
                check_color = QColor("#1C1C1C")  # 深底色，对勾清晰

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(fill_color))
            painter.drawRoundedRect(checkbox_rect, 3, 3)

            # 绘制打勾
            painter.setPen(QPen(check_color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(4, 9, 7, 12)
            painter.drawLine(7, 12, 13, 5)
        else:
            # 未选中状态：只绘制边框
            if is_light_theme:
                border_color = QColor("#D1D5DB")
            else:
                border_color = QColor("#4A4A4A")  # 中灰边框（与 border2 统一）

            painter.setPen(QPen(border_color, 1.5))
            painter.setBrush(bg_color)
            painter.drawRoundedRect(checkbox_rect, 3, 3)

        # 绘制文字
        text_rect = QRect(28, 0, self.width() - 28, self.height())
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.text())

        painter.end()

    def mousePressEvent(self, event):
        """处理点击"""
        if event.button() == Qt.LeftButton:
            checkbox_rect = QRect(0, (self.height() - 18) // 2, 18, 18)
            if checkbox_rect.contains(event.pos()):
                self.setChecked(not self.isChecked())
                return
        super().mousePressEvent(event)

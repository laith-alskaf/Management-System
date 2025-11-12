# -*- coding: utf-8 -*-

"""
وحدة الثيمات للهوية البصرية السورية
"""

from PyQt6.QtGui import QFont, QFontDatabase

class SyrianThemes:
    """
    فئة تحتوي على الثيمات والأنماط البصرية للتطبيق.
    """

    # تعريف الألوان الأساسية للهوية البصرية
    COLOR_RED = "#CE1126"       # أحمر العلم السوري
    COLOR_WHITE = "#FFFFFF"     # أبيض
    COLOR_BLACK = "#000000"     # أسود العلم السوري
    COLOR_GREEN = "#007A3D"     # أخضر العلم السوري

    # ألوان ثانوية لتصميم عصري
    COLOR_LIGHT_GRAY = "#F0F0F0" # رمادي فاتح للخلفيات
    COLOR_DARK_GRAY = "#333333"  # رمادي غامق للنصوص
    COLOR_HOVER_RED = "#A40E1E"  # درجة أغمق من الأحمر عند المرور

    @staticmethod
    def apply_fonts():
        """
        يقوم بتحميل وتطبيق الخطوط العربية المخصصة.
        يمكن إضافة خطوط مخصصة هنا في المستقبل.
        """
        # استخدام خطوط النظام المتاحة حاليًا
        font = QFont("Simplified Arabic")
        return font

    @staticmethod
    def get_main_stylesheet():
        """
        يُرجع ورقة الأنماط الرئيسية (QSS) للتطبيق.

        Returns:
            str: سلسلة نصية تحتوي على كود QSS.
        """
        return f"""
            /* ======== النمط العام ======== */
            QWidget {{
                background-color: {SyrianThemes.COLOR_WHITE};
                color: {SyrianThemes.COLOR_DARK_GRAY};
                font-family: "Simplified Arabic", "Tahoma";
                font-size: 14px;
            }}

            /* ======== شريط العنوان والنوافذ ======== */
            QMainWindow, QDialog {{
                background-color: {SyrianThemes.COLOR_LIGHT_GRAY};
            }}

            /* ======== حقول الإدخال ======== */
            QLineEdit, QTextEdit, QSpinBox {{
                background-color: {SyrianThemes.COLOR_WHITE};
                border: 1px solid {SyrianThemes.COLOR_GREEN};
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }}
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{
                border: 2px solid {SyrianThemes.COLOR_GREEN};
            }}

            /* ======== الأزرار ======== */
            QPushButton {{
                background-color: {SyrianThemes.COLOR_RED};
                color: {SyrianThemes.COLOR_WHITE};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: {SyrianThemes.COLOR_HOVER_RED};
            }}
            QPushButton:pressed {{
                background-color: {SyrianThemes.COLOR_RED};
            }}
            QPushButton:disabled {{
                background-color: #AAAAAA;
            }}

            /* ======== الجداول ======== */
            QTableView {{
                border: 1px solid {SyrianThemes.COLOR_GREEN};
                gridline-color: #DDDDDD;
                background-color: {SyrianThemes.COLOR_WHITE};
            }}
            QHeaderView::section {{
                background-color: {SyrianThemes.COLOR_GREEN};
                color: {SyrianThemes.COLOR_WHITE};
                padding: 8px;
                border: 1px solid {SyrianThemes.COLOR_GREEN};
                font-weight: bold;
            }}
            QTableView::item:alternate {{
                background-color: {SyrianThemes.COLOR_LIGHT_GRAY};
            }}
            QTableView::item:selected {{
                background-color: {SyrianThemes.COLOR_RED};
                color: {SyrianThemes.COLOR_WHITE};
            }}

            /* ======== شريط التمرير ======== */
            QScrollBar:vertical {{
                border: none;
                background: {SyrianThemes.COLOR_LIGHT_GRAY};
                width: 12px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #CCCCCC;
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #BBBBBB;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {SyrianThemes.COLOR_LIGHT_GRAY};
                height: 12px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: #CCCCCC;
                min-width: 20px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: #BBBBBB;
            }}
        """

# مثال للاستخدام (لأغراض الاختبار)
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableView
    import sys

    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("اختبار الثيم السوري")
    window.setLayout(QVBoxLayout())

    style_sheet = SyrianThemes.get_main_stylesheet()
    app.setStyleSheet(style_sheet)

    window.layout().addWidget(QLineEdit("...اكتب هنا"))
    window.layout().addWidget(QPushButton("زر أحمر"))
    window.layout().addWidget(QTableView())

    window.resize(400, 300)
    window.show()

    sys.exit(app.exec())

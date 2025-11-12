# -*- coding: utf-8 -*-

"""
واجهة المستخدم للوحة التحكم الرئيسية
"""

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSpacerItem, QSizePolicy, QStackedWidget)
from PyQt6.QtCore import Qt, QLocale, QSize
from PyQt6.QtGui import QIcon

# المسارات النسبية قد تحتاج إلى تعديل عند التشغيل من main.py
from utils.syrian_themes import SyrianThemes

class DashboardView(QMainWindow):
    """
    فئة واجهة لوحة التحكم الرئيسية.
    """
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """
        تقوم بتهيئة واجهة المستخدم.
        """
        # تعيين اللغة والتخطيط
        self.setLocale(QLocale(QLocale.Language.Arabic))
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # إعدادات النافذة
        self.setWindowTitle("لوحة التحكم الرئيسية - نظام إدارة المشتريات الوطني السوري")
        self.resize(1200, 800)

        # الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # التخطيط الرئيسي
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- قائمة التنقل الجانبية (Sidebar) ---
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            background-color: #007A3D; /* أخضر */
            color: white;
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(20)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # عنوان السايدبار
        title_label = QLabel("القائمة الرئيسية")
        title_label.setFont(self.font_with_size(18, bold=True))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_label)

        # أزرار التنقل
        self.suppliers_button = self.create_nav_button("إدارة الموردين")
        self.materials_button = self.create_nav_button("إدارة المواد")
        self.orders_button = self.create_nav_button("إدارة الطلبات")
        self.reports_button = self.create_nav_button("التقارير")

        sidebar_layout.addWidget(self.suppliers_button)
        sidebar_layout.addWidget(self.materials_button)
        sidebar_layout.addWidget(self.orders_button)
        sidebar_layout.addWidget(self.reports_button)

        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.logout_button = self.create_nav_button("تسجيل الخروج")
        sidebar_layout.addWidget(self.logout_button)

        main_layout.addWidget(sidebar)

        # --- منطقة المحتوى الرئيسية (باستخدام QStackedWidget) ---
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # الواجهة الرئيسية (الافتراضية)
        welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(welcome_widget)
        welcome_layout.setContentsMargins(40, 40, 40, 40)
        welcome_layout.setSpacing(25)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        welcome_label = QLabel("أهلاً بك في نظام إدارة المشتريات الوطني السوري")
        welcome_label.setFont(self.font_with_size(24, bold=True))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        welcome_layout.addWidget(welcome_label)

        info_label = QLabel("الرجاء تحديد خيار من القائمة الجانبية للبدء.")
        info_label.setFont(self.font_with_size(16))
        info_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        welcome_layout.addWidget(info_label)

        self.stacked_widget.addWidget(welcome_widget)

    def create_nav_button(self, text):
        """
        ينشئ زر تنقل مخصص للسايدبار.
        """
        button = QPushButton(text)
        button.setFont(self.font_with_size(14, bold=True))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 12px;
                text-align: right;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        return button

    def font_with_size(self, size, bold=False):
        """
        يُرجع خطًا بالحجم والوزن المطلوبين.
        """
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

# كود للاختبار المستقل
if __name__ == '__main__':
    from utils.syrian_themes import SyrianThemes
    app = QApplication(sys.argv)

    # تطبيق الثيم الرئيسي
    style_sheet = SyrianThemes.get_main_stylesheet()
    app.setStyleSheet(style_sheet)

    dashboard = DashboardView()
    dashboard.show()
    sys.exit(app.exec())

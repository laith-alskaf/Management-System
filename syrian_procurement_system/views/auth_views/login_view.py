# -*- coding: utf-8 -*-

"""
واجهة المستخدم لتسجيل الدخول
"""

import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QCheckBox, QApplication, QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QLocale

class LoginView(QWidget):
    """
    فئة واجهة تسجيل الدخول.
    """
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """
        تقوم بتهيئة واجهة المستخدم.
        """
        # تعيين اللغة العربية
        self.setLocale(QLocale(QLocale.Language.Arabic))
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # إعدادات النافذة
        self.setWindowTitle("تسجيل الدخول - نظام إدارة المشتريات الوطني السوري")
        self.setFixedSize(400, 450)

        # الألوان والخطوط (مستوحاة من الهوية السورية)
        primary_font = QFont("Simplified Arabic", 12)
        title_font = QFont("Simplified Arabic", 16, QFont.Weight.Bold)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF; /* أبيض */
            }
            QLabel {
                color: #000000; /* أسود */
            }
            QLineEdit {
                border: 1px solid #007A3D; /* أخضر */
                padding: 8px;
                border-radius: 5px;
                background-color: #F0F0F0;
            }
            QPushButton {
                background-color: #CE1126; /* أحمر */
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A40E1E;
            }
            QCheckBox {
                color: #000000;
            }
        """)

        # التخطيط الرئيسي
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # الشعار (مؤقت)
        # يمكنك استبدال "path/to/syrian_logo.png" بالمسار الفعلي للشعار
        logo_label = QLabel(self)
        # pixmap = QPixmap("path/to/syrian_logo.png").scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        # logo_label.setPixmap(pixmap)
        logo_label.setText("شعار وطني هنا") # نص مؤقت بدلاً من الصورة
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFont(QFont("Arial", 14))
        layout.addWidget(logo_label)

        # عنوان الواجهة
        title_label = QLabel("نظام إدارة المشتريات الوطني السوري")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # حقل البريد الإلكتروني
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("البريد الإلكتروني")
        self.email_input.setFont(primary_font)
        self.email_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.email_input)

        # حقل كلمة المرور
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setFont(primary_font)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.password_input)

        # خيار "تذكرني"
        self.remember_me_checkbox = QCheckBox("تذكرني")
        self.remember_me_checkbox.setFont(primary_font)
        layout.addWidget(self.remember_me_checkbox)

        # زر تسجيل الدخول
        self.login_button = QPushButton("تسجيل الدخول")
        self.login_button.setFont(primary_font)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.login_button)

        # رسالة الخطأ (مخفية بشكل افتراضي)
        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Simplified Arabic", 10))
        self.error_label.setStyleSheet("color: #CE1126;") # أحمر
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        self.error_label.hide()

        # إضافة مساحة فارغة لدفع العناصر للأعلى
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

# الكود التالي لتشغيل الواجهة بشكل مستقل للاختبار
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_view = LoginView()
    login_view.show()
    sys.exit(app.exec())

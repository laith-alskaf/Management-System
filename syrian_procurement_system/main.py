# -*- coding: utf-8 -*-

"""
نقطة الدخول الرئيسية لنظام إدارة المشتريات الوطني السوري.
"""

import sys
from PyQt6.QtWidgets import QApplication
from syrian_procurement_system.controllers.auth_controller import AuthController
from syrian_procurement_system.utils.syrian_themes import SyrianThemes

def main():
    """
    الوظيفة الرئيسية التي تقوم بتشغيل التطبيق.
    """
    app = QApplication(sys.argv)

    # تطبيق الثيم المركزي على التطبيق بالكامل
    style_sheet = SyrianThemes.get_main_stylesheet()
    app.setStyleSheet(style_sheet)

    # إنشاء وتشغيل وحدة التحكم الخاصة بالمصادقة
    auth_controller = AuthController()
    auth_controller.show_login()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

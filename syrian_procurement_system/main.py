# -*- coding: utf-8 -*-

"""
نقطة الدخول الرئيسية لنظام إدارة المشتريات الوطني السوري.
"""

import sys
from PyQt6.QtWidgets import QApplication
from syrian_procurement_system.controllers.auth_controller import AuthController

def main():
    """
    الوظيفة الرئيسية التي تقوم بتشغيل التطبيق.
    """
    app = QApplication(sys.argv)

    # إنشاء وتشغيل وحدة التحكم الخاصة بالمصادقة
    auth_controller = AuthController()
    auth_controller.show_login()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

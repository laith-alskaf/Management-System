# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بلوحة التحكم الرئيسية
"""

# المسارات النسبية قد تحتاج إلى تعديل عند التشغيل من main.py
from views.main_views.dashboard_view import DashboardView

class DashboardController:
    """
    فئة وحدة التحكم للوحة التحكم الرئيسية.
    """
    def __init__(self, logout_callback=None):
        self.view = DashboardView(self)
        self.logout_callback = logout_callback
        self._connect_signals()

    def _connect_signals(self):
        """
        يربط إشارات الواجهة (مثل نقرات الأزرار) بالوظائف المناسبة.
        """
        # سيتم ربط إشارات أزرار التنقل هنا في المستقبل
        # self.view.suppliers_button.clicked.connect(self.show_suppliers)
        # self.view.materials_button.clicked.connect(self.show_materials)
        # self.view.orders_button.clicked.connect(self.show_orders)
        self.view.logout_button.clicked.connect(self.handle_logout)

    def show(self):
        """
        يعرض واجهة لوحة التحكم الرئيسية.
        """
        self.view.show()

    def handle_logout(self):
        """
        يعالج منطق تسجيل الخروج.
        """
        self.view.close()
        if self.logout_callback:
            self.logout_callback()

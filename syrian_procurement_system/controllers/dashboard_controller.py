# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بلوحة التحكم الرئيسية
"""

from views.main_views.dashboard_view import DashboardView
from controllers.supplier_controller import SupplierController
from controllers.material_controller import MaterialController

class DashboardController:
    """
    فئة وحدة التحكم للوحة التحكم الرئيسية.
    """
    def __init__(self, logout_callback=None):
        self.view = DashboardView(self)
        self.logout_callback = logout_callback

        # تهيئة وحدات التحكم الفرعية
        self.supplier_controller = SupplierController()
        self.material_controller = MaterialController()

        # إضافة الواجهات إلى QStackedWidget
        self.view.stacked_widget.addWidget(self.supplier_controller.get_view())
        self.view.stacked_widget.addWidget(self.material_controller.get_view())

        self._connect_signals()

    def _connect_signals(self):
        """
        يربط إشارات الواجهة (مثل نقرات الأزرار) بالوظائف المناسبة.
        """
        self.view.suppliers_button.clicked.connect(self.show_suppliers)
        self.view.materials_button.clicked.connect(self.show_materials)
        # self.view.orders_button.clicked.connect(self.show_orders)
        self.view.logout_button.clicked.connect(self.handle_logout)

    def show_suppliers(self):
        """
        يعرض واجهة إدارة الموردين.
        """
        self.view.stacked_widget.setCurrentWidget(self.supplier_controller.get_view())

    def show_materials(self):
        """
        يعرض واجهة إدارة المواد.
        """
        self.view.stacked_widget.setCurrentWidget(self.material_controller.get_view())

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

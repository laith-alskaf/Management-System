# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بالموردين
"""

from services.local_db_service import LocalDbService
from views.main_views.suppliers_view import SuppliersView, SupplierDialog
from models.supplier_model import Supplier

class SupplierController:
    """
    فئة وحدة التحكم لإدارة الموردين.
    """
    def __init__(self):
        self.db_service = LocalDbService()
        self.view = SuppliersView(self)
        self._connect_signals()
        self.load_suppliers()

    def _connect_signals(self):
        """
        يربط إشارات الواجهة بوظائف المتحكم.
        """
        self.view.add_button.clicked.connect(self.show_add_dialog)
        self.view.edit_button.clicked.connect(self.show_edit_dialog)
        self.view.delete_button.clicked.connect(self.delete_supplier)

    def get_view(self):
        """
        تُرجع الواجهة التي يديرها هذا المتحكم.
        """
        return self.view

    def load_suppliers(self):
        """
        تحميل قائمة الموردين من قاعدة البيانات وعرضها في الجدول.
        """
        suppliers = self.db_service.get_all_suppliers()
        self.view.set_table_data(suppliers)

    def show_add_dialog(self):
        """
        يعرض نافذة إضافة مورد جديد.
        """
        dialog = SupplierDialog()
        if dialog.exec():
            data = dialog.get_data()
            if not data['name']:
                self.view.show_error("خطأ في الإدخال", "اسم المورد حقل إلزامي.")
                return
            self.db_service.add_supplier(**data)
            self.load_suppliers() # إعادة تحميل البيانات لتحديث الجدول
            self.view.show_message("نجاح", "تمت إضافة المورد بنجاح.")

    def show_edit_dialog(self):
        """
        يعرض نافذة تعديل بيانات المورد المحدد.
        """
        supplier_id = self.view.get_selected_supplier_id()
        if supplier_id is None:
            self.view.show_error("خطأ", "الرجاء تحديد مورد لتعديله.")
            return

        supplier = self.db_service.db.get(Supplier, supplier_id)

        dialog = SupplierDialog(supplier=supplier)
        if dialog.exec():
            data = dialog.get_data()
            if not data['name']:
                self.view.show_error("خطأ في الإدخال", "اسم المورد حقل إلزامي.")
                return
            self.db_service.update_supplier(supplier_id, **data)
            self.load_suppliers()
            self.view.show_message("نجاح", "تم تحديث بيانات المورد بنجاح.")

    def delete_supplier(self):
        """
        يحذف المورد المحدد من قاعدة البيانات.
        """
        supplier_id = self.view.get_selected_supplier_id()
        if supplier_id is None:
            self.view.show_error("خطأ", "الرجاء تحديد مورد لحذفه.")
            return

        if self.view.show_confirm_dialog("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا المورد؟"):
            self.db_service.delete_supplier(supplier_id)
            self.load_suppliers()
            self.view.show_message("نجاح", "تم حذف المورد بنجاح.")

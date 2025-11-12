# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بإدارة الموردين
"""

from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMessageBox, QApplication
from services.local_db_service import LocalDbService
from views.main_views.suppliers_view import SuppliersView, SupplierDialog
from utils.worker import Worker

class SupplierController:
    """
    فئة وحدة التحكم للموردين.
    """
    def __init__(self):
        self.db_service = LocalDbService()
        self.view = SuppliersView(self)
        self.thread_pool = QThreadPool.globalInstance()
        self._connect_signals()
        self._load_suppliers()

    def get_view(self):
        """
        تُرجع الواجهة التي تديرها وحدة التحكم هذه.
        """
        return self.view

    def _connect_signals(self):
        """
        تربط إشارات الواجهة بالوظائف المناسبة.
        """
        self.view.add_button.clicked.connect(self._add_supplier_dialog)
        self.view.edit_button.clicked.connect(self._edit_supplier_dialog)
        self.view.delete_button.clicked.connect(self._delete_supplier)

    def _run_task(self, task_fn, *args, on_success_msg):
        """
        يشغل مهمة في خيط منفصل ويعالج النتائج.
        """
        self._set_loading_state(True)
        worker = Worker(task_fn, *args)
        worker.signals.result.connect(lambda result: self._on_task_success(on_success_msg))
        worker.signals.error.connect(self._on_task_error)
        worker.signals.finished.connect(lambda: self._set_loading_state(False))
        self.thread_pool.start(worker)

    def _on_task_success(self, message):
        """
        يتم استدعاؤها عند نجاح المهمة.
        """
        self._load_suppliers()
        self.view.show_message("نجاح", message)

    def _on_task_error(self, error_details):
        """
        يتم استدعاؤها عند فشل المهمة.
        """
        ex_type, ex_value, _ = error_details
        error_message = f"فشلت العملية. قد يكون الاسم أو البريد الإلكتروني مسجلاً مسبقاً.\nالتفاصيل: {ex_value}"
        self.view.show_message("خطأ", error_message, is_error=True)

    def _load_suppliers(self):
        """
        تحميل بيانات الموردين من قاعدة البيانات وعرضها في الجدول.
        """
        self._set_loading_state(True)
        worker = Worker(self.db_service.get_all_suppliers)
        worker.signals.result.connect(self._on_load_suppliers_result)
        worker.signals.error.connect(self._on_task_error)
        worker.signals.finished.connect(lambda: self._set_loading_state(False))
        self.thread_pool.start(worker)

    def _on_load_suppliers_result(self, suppliers):
        """
        يتم استدعاؤها عند نجاح تحميل الموردين.
        """
        self.view.populate_table(suppliers)

    def _add_supplier_dialog(self):
        """
        تفتح نافذة لإضافة مورد جديد.
        """
        dialog = SupplierDialog(parent=self.view)
        if dialog.exec():
            data = dialog.get_data()
            if not data['name']:
                self.view.show_message("خطأ في الإدخال", "اسم المورد حقل إلزامي.", is_error=True)
                return
            self._run_task(self.db_service.add_supplier, **data, on_success_msg="تمت إضافة المورد بنجاح.")

    def _edit_supplier_dialog(self):
        """
        تفتح نافذة لتعديل المورد المحدد.
        """
        supplier_id = self.view.get_selected_supplier_id()
        if supplier_id is None:
            return

        supplier = self.db_service.get_supplier_by_id(supplier_id)
        if not supplier:
            self.view.show_message("خطأ", "المورد المحدد غير موجود.", is_error=True)
            return

        supplier_data = {
            'name': supplier.name, 'contact_person': supplier.contact_person, 'phone': supplier.phone,
            'email': supplier.email, 'address': supplier.address
        }

        dialog = SupplierDialog(supplier_data=supplier_data, parent=self.view)
        if dialog.exec():
            new_data = dialog.get_data()
            if not new_data['name']:
                self.view.show_message("خطأ في الإدخال", "اسم المورد حقل إلزامي.", is_error=True)
                return
            self._run_task(self.db_service.update_supplier, supplier_id, **new_data, on_success_msg="تم تحديث بيانات المورد بنجاح.")

    def _delete_supplier(self):
        """
        تحذف المورد المحدد بعد التأكيد.
        """
        supplier_id = self.view.get_selected_supplier_id()
        if supplier_id is None:
            return

        reply = QMessageBox.question(self.view, 'تأكيد الحذف',
                                     'هل أنت متأكد أنك تريد حذف هذا المورد؟',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self._run_task(self.db_service.delete_supplier, supplier_id, on_success_msg="تم حذف المورد بنجاح.")

    def _set_loading_state(self, is_loading):
        """
        تغيير حالة واجهة المستخدم لتعكس حالة التحميل.
        """
        buttons = [self.view.add_button, self.view.edit_button, self.view.delete_button]
        for button in buttons:
            button.setEnabled(not is_loading)

        QApplication.instance().processEvents()

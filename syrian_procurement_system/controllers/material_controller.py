# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بإدارة المواد
"""

from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMessageBox, QApplication
from services.local_db_service import LocalDbService
from views.main_views.materials_view import MaterialsView, MaterialDialog
from utils.worker import Worker

class MaterialController:
    """
    فئة وحدة التحكم للمواد.
    """
    def __init__(self):
        self.view = MaterialsView(self)
        self.thread_pool = QThreadPool.globalInstance()
        self._connect_signals()

    def get_view(self):
        return self.view

    def _connect_signals(self):
        self.view.add_button.clicked.connect(self._add_material_dialog)
        self.view.edit_button.clicked.connect(self._edit_material_dialog)
        self.view.delete_button.clicked.connect(self._delete_material)

    def _run_task(self, task_fn, *args, on_success_msg, **kwargs):
        self._set_loading_state(True)
        worker = Worker(task_fn, *args, **kwargs)
        worker.signals.result.connect(lambda result: self._on_task_success(on_success_msg))
        worker.signals.error.connect(self._on_task_error)
        worker.signals.finished.connect(lambda: self._set_loading_state(False))
        self.thread_pool.start(worker)

    def _on_task_success(self, message):
        if message:
            self.view.show_message("نجاح", message)
        self.load_materials()

    def _on_task_error(self, error_details):
        ex_type, ex_value, _ = error_details
        error_message = f"فشلت العملية. قد يكون اسم المادة مسجلاً مسبقاً.\nالتفاصيل: {ex_value}"
        self.view.show_message("خطأ", error_message, is_error=True)
        self._set_loading_state(False)

    def load_materials(self):
        worker = Worker(LocalDbService.get_all_materials)
        worker.signals.result.connect(self._on_load_materials_result)
        worker.signals.error.connect(self._on_task_error)
        self.thread_pool.start(worker)

    def _on_load_materials_result(self, materials):
        self.view.populate_table(materials)

    def _add_material_dialog(self):
        dialog = MaterialDialog(parent=self.view)
        if dialog.exec():
            data = dialog.get_data()
            if not data['name']:
                self.view.show_message("خطأ في الإدخال", "اسم المادة حقل إلزامي.", is_error=True)
                return
            self._run_task(LocalDbService.add_material, **data, on_success_msg="تمت إضافة المادة بنجاح.")

    def _edit_material_dialog(self):
        material_id = self.view.get_selected_material_id()
        if material_id is None:
            return

        material = LocalDbService.get_material_by_id(material_id)
        if not material:
            self.view.show_message("خطأ", "المادة المحددة غير موجودة.", is_error=True)
            return

        material_data = {
            'name': material.name, 'category': material.category, 'quantity': material.quantity,
            'price': material.price, 'expiry_date': material.expiry_date
        }

        dialog = MaterialDialog(material_data=material_data, parent=self.view)
        if dialog.exec():
            new_data = dialog.get_data()
            if not new_data['name']:
                self.view.show_message("خطأ في الإدخال", "اسم المادة حقل إلزامي.", is_error=True)
                return
            self._run_task(LocalDbService.update_material, material_id, **new_data, on_success_msg="تم تحديث بيانات المادة بنجاح.")

    def _delete_material(self):
        material_id = self.view.get_selected_material_id()
        if material_id is None:
            return

        reply = QMessageBox.question(self.view, 'تأكيد الحذف',
                                     'هل أنت متأكد أنك تريد حذف هذه المادة؟',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self._run_task(LocalDbService.delete_material, material_id, on_success_msg="تم حذف المادة بنجاح.")

    def _set_loading_state(self, is_loading):
        buttons = [self.view.add_button, self.view.edit_button, self.view.delete_button]
        for button in buttons:
            button.setEnabled(not is_loading)
        QApplication.instance().processEvents()

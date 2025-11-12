# -*- coding: utf-8 -*-

"""
واجهة المستخدم لإدارة الموردين
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableView, QAbstractItemView, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont

class SupplierTableModel(QAbstractTableModel):
    """
    نموذج بيانات لجدول الموردين.
    """
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["المعرف", "اسم المورد", "جهة الاتصال", "الهاتف", "العنوان"]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            supplier = self._data[index.row()]
            return [supplier.id, supplier.name, supplier.contact_person, supplier.phone, supplier.address][index.column()]
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

class SuppliersView(QWidget):
    """
    فئة واجهة إدارة الموردين.
    """
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """
        تقوم بتهيئة واجهة المستخدم.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # شريط الأزرار
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.add_button = QPushButton("إضافة مورد جديد")
        self.edit_button = QPushButton("تعديل المورد المحدد")
        self.delete_button = QPushButton("حذف المورد المحدد")

        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        # جدول الموردين
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        layout.addWidget(self.table_view)

    def set_table_data(self, data):
        """
        تُعين البيانات لنموذج الجدول.
        """
        model = SupplierTableModel(data)
        self.table_view.setModel(model)
        # إخفاء عمود المعرف (ID)
        self.table_view.setColumnHidden(0, True)

    def get_selected_supplier_id(self):
        """
        تُرجع معرف المورد المحدد في الجدول.
        """
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            return None
        # نحصل على النموذج من الجدول
        model = self.table_view.model()
        # نحصل على الفهرس لعمود المعرف (0) للصف المحدد
        id_index = model.index(selected_indexes[0].row(), 0)
        return model.data(id_index, Qt.ItemDataRole.DisplayRole)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_confirm_dialog(self, title, message):
        reply = QMessageBox.question(self, title, message,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes

from PyQt6.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox

class SupplierDialog(QDialog):
    """
    نافذة منبثقة لإضافة أو تعديل بيانات مورد.
    """
    def __init__(self, supplier=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("بيانات المورد")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.name_input = QLineEdit()
        self.contact_person_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        if supplier:
            self.name_input.setText(supplier.name)
            self.contact_person_input.setText(supplier.contact_person or "")
            self.phone_input.setText(supplier.phone or "")
            self.address_input.setText(supplier.address or "")

        form_layout = QFormLayout()
        form_layout.addRow("اسم المورد:", self.name_input)
        form_layout.addRow("جهة الاتصال:", self.contact_person_input)
        form_layout.addRow("الهاتف:", self.phone_input)
        form_layout.addRow("العنوان:", self.address_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "contact_person": self.contact_person_input.text(),
            "phone": self.phone_input.text(),
            "address": self.address_input.text()
        }

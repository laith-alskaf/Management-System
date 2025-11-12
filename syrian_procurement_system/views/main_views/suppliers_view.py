# -*- coding: utf-8 -*-

"""
واجهة المستخدم الخاصة بإدارة الموردين
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QLineEdit, QDialog, QDialogButtonBox,
                             QFormLayout, QMessageBox, QHeaderView, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SuppliersView(QWidget):
    """
    الواجهة الرئيسية لعرض وإدارة الموردين.
    """
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # عنوان الواجهة
        title_label = QLabel("إدارة الموردين")
        title_font = QFont("Simplified Arabic", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(title_label)

        # أزرار الإجراءات (إضافة، تعديل، حذف)
        actions_layout = QHBoxLayout()
        self.add_button = QPushButton("إضافة مورد جديد")
        self.edit_button = QPushButton("تعديل المورد المحدد")
        self.delete_button = QPushButton("حذف المورد المحدد")

        actions_layout.addWidget(self.add_button)
        actions_layout.addWidget(self.edit_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addStretch()
        main_layout.addLayout(actions_layout)

        # جدول عرض الموردين
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["المعرف", "اسم المورد", "الشخص المسؤول", "الهاتف", "العنوان"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.table)

    def populate_table(self, suppliers):
        """
        تملأ الجدول ببيانات الموردين.
        """
        self.table.setRowCount(len(suppliers))
        for row, supplier in enumerate(suppliers):
            self.table.setItem(row, 0, QTableWidgetItem(str(supplier.id)))
            self.table.setItem(row, 1, QTableWidgetItem(supplier.name))
            self.table.setItem(row, 2, QTableWidgetItem(supplier.contact_person))
            self.table.setItem(row, 3, QTableWidgetItem(supplier.phone))
            self.table.setItem(row, 4, QTableWidgetItem(supplier.address))
        # إخفاء عمود المعرف (id)
        self.table.setColumnHidden(0, True)

    def get_selected_supplier_id(self):
        """
        تُرجع معرف المورد المحدد في الجدول.
        """
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_message("خطأ", "الرجاء تحديد مورد أولاً.")
            return None
        # row index of the first selected item
        row_index = selected_rows[0].row()
        supplier_id_item = self.table.item(row_index, 0)
        return int(supplier_id_item.text())

    def show_message(self, title, message, is_error=False):
        """
        تعرض رسالة للمستخدم.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning if is_error else QMessageBox.Icon.Information)
        msg_box.exec()

class SupplierDialog(QDialog):
    """
    نافذة حوار لإضافة أو تعديل بيانات مورد.
    """
    def __init__(self, supplier_data=None, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setWindowTitle("بيانات المورد")
        self.setMinimumWidth(400)

        self.form_layout = QFormLayout(self)
        self.form_layout.setContentsMargins(20, 20, 20, 20)
        self.form_layout.setSpacing(15)

        # حقول الإدخال
        self.name_input = QLineEdit()
        self.contact_person_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        # إضافة الحقول إلى النموذج مع تسميات عربية
        self.form_layout.addRow("اسم المورد:", self.name_input)
        self.form_layout.addRow("الشخص المسؤول:", self.contact_person_input)
        self.form_layout.addRow("رقم الهاتف:", self.phone_input)
        self.form_layout.addRow("البريد الإلكتروني:", self.email_input)
        self.form_layout.addRow("العنوان:", self.address_input)

        # إذا كان هناك بيانات مورد (في حالة التعديل)، قم بملء الحقول
        if supplier_data:
            self.name_input.setText(supplier_data.get('name', ''))
            self.contact_person_input.setText(supplier_data.get('contact_person', ''))
            self.phone_input.setText(supplier_data.get('phone', ''))
            self.email_input.setText(supplier_data.get('email', ''))
            self.address_input.setText(supplier_data.get('address', ''))

        # أزرار الحفظ والإلغاء
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # تغيير نصوص الأزرار إلى العربية
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("حفظ")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("إلغاء")

        self.form_layout.addRow(self.button_box)

    def get_data(self):
        """
        تُرجع البيانات المدخلة في النموذج.
        """
        return {
            "name": self.name_input.text().strip(),
            "contact_person": self.contact_person_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "email": self.email_input.text().strip(),
            "address": self.address_input.text().strip()
        }

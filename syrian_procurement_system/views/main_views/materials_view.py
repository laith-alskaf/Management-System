# -*- coding: utf-8 -*-

"""
واجهة المستخدم الخاصة بإدارة المواد
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QLabel, QLineEdit, QDialog, QDialogButtonBox,
                             QFormLayout, QMessageBox, QHeaderView, QSizePolicy, QDateEdit)
from PyQt6.QtCore import Qt, QDate

class MaterialsView(QWidget):
    """
    الواجهة الرئيسية لعرض وإدارة المواد.
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

        title_label = QLabel("إدارة المواد")
        title_label.setFont(self.font().setPointSizeF(20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(title_label)

        actions_layout = QHBoxLayout()
        self.add_button = QPushButton("إضافة مادة جديدة")
        self.edit_button = QPushButton("تعديل المادة المحددة")
        self.delete_button = QPushButton("حذف المادة المحددة")

        actions_layout.addWidget(self.add_button)
        actions_layout.addWidget(self.edit_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addStretch()
        main_layout.addLayout(actions_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["المعرف", "اسم المادة", "التصنيف", "الكمية", "السعر", "تاريخ الصلاحية"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.table)

    def populate_table(self, materials):
        """
        تملأ الجدول ببيانات المواد.
        """
        self.table.setRowCount(len(materials))
        for row, material in enumerate(materials):
            self.table.setItem(row, 0, QTableWidgetItem(str(material.id)))
            self.table.setItem(row, 1, QTableWidgetItem(material.name))
            self.table.setItem(row, 2, QTableWidgetItem(material.category))
            self.table.setItem(row, 3, QTableWidgetItem(str(material.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(str(material.price)))
            expiry_date_str = material.expiry_date.strftime('%Y-%m-%d') if material.expiry_date else "لا يوجد"
            self.table.setItem(row, 5, QTableWidgetItem(expiry_date_str))
        self.table.setColumnHidden(0, True)

    def get_selected_material_id(self):
        """
        تُرجع معرف المادة المحددة في الجدول.
        """
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_message("خطأ", "الرجاء تحديد مادة أولاً.")
            return None
        row_index = selected_rows[0].row()
        material_id_item = self.table.item(row_index, 0)
        return int(material_id_item.text())

    def show_message(self, title, message, is_error=False):
        """
        تعرض رسالة للمستخدم.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning if is_error else QMessageBox.Icon.Information)
        msg_box.exec()

class MaterialDialog(QDialog):
    """
    نافذة حوار لإضافة أو تعديل بيانات مادة.
    """
    def __init__(self, material_data=None, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setWindowTitle("بيانات المادة")
        self.setMinimumWidth(400)

        self.form_layout = QFormLayout(self)
        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        self.expiry_date_input = QDateEdit()
        self.expiry_date_input.setCalendarPopup(True)
        self.expiry_date_input.setDisplayFormat("yyyy-MM-dd")

        self.form_layout.addRow("اسم المادة:", self.name_input)
        self.form_layout.addRow("التصنيف:", self.category_input)
        self.form_layout.addRow("الكمية:", self.quantity_input)
        self.form_layout.addRow("السعر:", self.price_input)
        self.form_layout.addRow("تاريخ الصلاحية:", self.expiry_date_input)

        if material_data:
            self.name_input.setText(material_data.get('name', ''))
            self.category_input.setText(material_data.get('category', ''))
            self.quantity_input.setText(str(material_data.get('quantity', '')))
            self.price_input.setText(str(material_data.get('price', '')))
            expiry_date = material_data.get('expiry_date')
            if expiry_date:
                self.expiry_date_input.setDate(QDate.fromString(str(expiry_date), "yyyy-MM-dd"))
            else:
                self.expiry_date_input.setDate(QDate.currentDate())

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("حفظ")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("إلغاء")
        self.form_layout.addRow(self.button_box)

    def get_data(self):
        """
        تُرجع البيانات المدخلة في النموذج.
        """
        return {
            "name": self.name_input.text().strip(),
            "category": self.category_input.text().strip(),
            "quantity": int(self.quantity_input.text()) if self.quantity_input.text().isdigit() else 0,
            "price": float(self.price_input.text()) if self.price_input.text().replace('.', '', 1).isdigit() else 0.0,
            "expiry_date": self.expiry_date_input.date().toPyDate()
        }

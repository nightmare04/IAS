
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, \
    QCheckBox

from custom_components.combo_box import GroupComboBox, SystemComboBox, AgregateComboBox
from data.data import PlaneBase, OtkazAgregateBase


class AddOtkazDialog(QDialog):
    def __init__(self, plane: PlaneBase, parent=None):
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle("Добавление отказавшего блока/агрегата")
        self.setModal(True)
        self.setFixedSize(350, 250)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_combo = AgregateComboBox()

        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)
        self.system_combo.currentTextChanged.connect(self.agregate_combo.set_filter)

        self.agregate_number = QLineEdit()
        self.remove_checkbox = QCheckBox()
        self.desc = QLineEdit()

        form_layout.addRow("Группа обслуживания:", self.group_combo)
        form_layout.addRow("Система самолета:", self.system_combo)
        form_layout.addRow("Агрегат/блок:", self.agregate_combo)
        form_layout.addRow("Номер блока/агрегата:", self.agregate_number)
        form_layout.addRow("Агрегат снят?", self.remove_checkbox)
        form_layout.addRow("Примечание:", self.desc)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox()
        self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_button = self.button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)

        self.save_button.clicked.connect(self.create_item)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def create_item(self):
        try:
            agregate = self.agregate_combo.currentData()

            OtkazAgregateBase.create(
                agregate=agregate,
                plane=self.plane.id,
                number=self.agregate_number.text(),
                removed=self.remove_checkbox.isChecked(),
                description=self.desc.text()
            )
            self.accept()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить агрегат/блок: {str(e)}")


class EditOtkazDialog(AddOtkazDialog):
    def __init__(self, otkaz_agregate: OtkazAgregateBase, parent=None):
        super().__init__(otkaz_agregate.plane, parent)
        self.otkaz_agregate = otkaz_agregate
        self.setWindowTitle('Изменить')
        self.save_button.clicked.disconnect()
        self.save_button.clicked.connect(self.edit_item)
        delete_button = self.button_box.addButton("Удалить", QDialogButtonBox.ButtonRole.DestructiveRole)
        delete_button.clicked.connect(self.delete_item)
        self.load_data()

    def load_data(self):
        self.group_combo.setCurrentText(self.otkaz_agregate.agregate.system.group.name)
        self.system_combo.setCurrentText(self.otkaz_agregate.agregate.system.name)
        self.agregate_combo.setCurrentText(self.otkaz_agregate.agregate.name)
        self.agregate_number.setText(self.otkaz_agregate.number)
        self.remove_checkbox.setChecked(self.otkaz_agregate.removed)
        self.desc.setText(self.otkaz_agregate.description)

    def edit_item(self):
        try:
            agregate = self.agregate_combo.currentData()
            item = self.otkaz_agregate
            item.agregate = agregate
            item.number = self.agregate_number.text()
            item.removed = self.remove_checkbox.isChecked()
            item.description = self.desc.text()
            item.save()
            self.accept()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить агрегат/блок: {str(e)}")

    def delete_item(self):
        try:
            item = self.otkaz_agregate
            item.delete_instance()

            self.accept()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить агрегат/блок: {str(e)}")

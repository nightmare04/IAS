from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QMessageBox

from data import GroupBase, PlaneBase, PlaneSystemBase, PlaneTypeBase, OtkazAgregateBase, AgregateBase


class AddOtkazDialog(QDialog):
    def __init__(self, plane: PlaneBase, parent=None):
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle("Добавление отказавшего блока/агрегата")
        self.setModal(True)
        self.setFixedSize(350, 250)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.group_combo = QComboBox()
        self.group_combo.addItem('Выберите группу обслуживания')
        self.group_combo.currentTextChanged.connect(self.load_system)
        groups = GroupBase.select().where(GroupBase.plane_type == self.plane.plane_type)
        for group in groups:
            self.group_combo.addItem(group.name, group.id)

        self.system_combo = QComboBox()
        self.system_combo.currentTextChanged.connect(self.load_agregate)

        self.agregate_combo = QComboBox()

        self.agregate_number = QLineEdit()
        self.desc = QLineEdit()


        form_layout.addRow("Группа обслуживания:", self.group_combo)
        form_layout.addRow("Система самолета:", self.system_combo)
        form_layout.addRow("Агрегат/блок:", self.agregate_combo)
        form_layout.addRow("Номер блока/агрегата:", self.agregate_number)
        form_layout.addRow("Примечание:", self.desc)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept_and_save)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def load_system(self):
        self.system_combo.clear()
        systems = PlaneSystemBase.select().where(PlaneSystemBase.group == self.group_combo.currentData())
        for system in systems:
            self.system_combo.addItem(system.name, system.id)

    def load_agregate(self):
        self.agregate_combo.clear()
        agregate_list = AgregateBase.select().where(AgregateBase.system == self.system_combo.currentData())
        for agregate in agregate_list:
            self.agregate_combo.addItem(agregate.name, agregate.id)



    def accept_and_save(self):
        try:
            agregate = self.agregate_combo.currentData()

            OtkazAgregateBase.create(
                agregate=agregate,
                plane=self.plane.id,
                number=self.agregate_number.text()
            )

            self.accept()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить агрегат/блок: {str(e)}")

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox

from data import GroupBase


class AddOtkazDialog(QDialog):
    def __init__(self, plane, parent=None):
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
        groups = GroupBase.select().where()

        self.system_combo = QComboBox()
        self.system_combo.addItem('Выберите систему самолета')

        self.agregate_number = QLineEdit()
        self.desc = QLineEdit()

    def load_system(self):
        categories = Category.select().order_by(Category.name)
        for category in categories:
            self.category_combo.addItem(category.name, category.id)

        form_layout.addRow("Категория:", self.category_combo)
        form_layout.addRow("Название:", self.system_edit)
        form_layout.addRow("Цвет:", self.agregate_number)
        form_layout.addRow("Цена:", self.desc)

        layout.addLayout(form_layout)

        self.desc.setValidator(QIntValidator(0, 1000000))

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept_and_save)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def accept_and_save(self):
        if not self.system_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название продукта!")
            return

        try:
            category_id = self.category_combo.currentData()
            category = Category.get(Category.id == category_id)

            Product.create(
                category=category,
                name=self.system_edit.text(),
                color=self.agregate_number.text(),
                price=int(self.desc.text() or 0)
            )

            self.accept()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить продукт: {str(e)}")

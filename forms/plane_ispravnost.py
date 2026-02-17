from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox, \
    QFrame, QGridLayout, QFormLayout, QLineEdit, QDialogButtonBox, QCheckBox

from custom_components.buttons import PlaneBtn
from custom_components.combo_box import AgregateComboBox, GroupComboBox, SystemComboBox
from custom_components.groups import PodrGroup
from custom_components.tables import IspravnostTableModel, IspravnostTable
from data.data import PlaneBase, GroupBase, OtkazAgregateBase, PodrazdBase


class IspravnostFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.podr_layout = QGridLayout()
        self.setLayout(self.podr_layout)
        self.load_data()

    def load_data(self):
        podr_data = PodrazdBase.select()
        for i, podr in enumerate(podr_data):
            group = PodrGroup(podr)
            group.open_signal.connect(self.open_dialog)
            row = i // 2
            col = i % 2
            self.podr_layout.addWidget(group, row, col)

    def open_dialog(self, btn:PlaneBtn):
        dialog = PlaneIspravnost(btn.plane)
        dialog.exec()
        btn.update_color()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.clear_layout(sublayout)

    def update_podr(self):
        self.clear_layout(self.podr_layout)
        self.load_data()


class PlaneIspravnost(QDialog):
    def __init__(self, plane: PlaneBase, parent=None, ):
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle(f"Исправность самолета {self.plane.plane_type.name} №{self.plane.bort_number}")
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.control_panel = QWidget()
        self.control_layout = QHBoxLayout(self.control_panel)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все группы")
        groups = GroupBase.select().order_by(GroupBase.name)
        for group in groups:
            self.filter_combo.addItem(group.name)
        self.filter_combo.currentTextChanged.connect(self.filter_by_category)

        self.add_btn = QPushButton("➕ Добавить блок / агрегат")
        self.add_btn.clicked.connect(self.add_item)

        self.control_layout.addWidget(QLabel("Фильтр по группе:"))
        self.control_layout.addWidget(self.filter_combo)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.add_btn)

        self.table_view = IspravnostTable(plane=plane)
        self.table_view.edit_signal.connect(self.edit_item)
        self.table_view.delete_signal.connect(self.delete_item)
        self.setup_ui()
        self.load_data()

    def filter_by_category(self, category):
        self.load_data(category_filter=category)

    def edit_item(self, item):
        dialog = AddOtkazDialog(plane=self.plane, item=item)
        if dialog.exec():
            self.refresh_data()
        
    def add_item(self):
        dialog = AddOtkazDialog(plane=self.plane)
        if dialog.exec():
            self.refresh_data()

    def delete_item(self, item):
        reply = QMessageBox.question(self, "Подтверждение удаления", "Вы уверены, что хотите удалить этот элемент?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                item.delete_instance()
                self.refresh_data()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить элемент: {str(e)}")

    def refresh_data(self):
        self.load_data()

    def on_double_click(self, index):
        model = self.table_view.model()
        if isinstance(model, IspravnostTableModel):
            item = model.get_item(index)
            if item:
                dialog = AddOtkazDialog(plane=self.plane, item=item)
                if dialog.exec():
                    self.refresh_data()

    def setup_ui(self):
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.table_view)

        # Настройка таблицы
        self.table_view.set_span_for_groups()
        self.table_view.setSortingEnabled(False)

        # Подключаем двойной клик
        self.table_view.doubleClicked.connect(self.on_double_click)

    def load_data(self, category_filter=None):
        self.table_view.table_model.load_data()
        self.table_view.set_span_for_groups()


class AddOtkazDialog(QDialog):
    def __init__(self, plane: PlaneBase, item: OtkazAgregateBase=None, parent=None):
        super().__init__(parent)
        self.plane = plane
        self.item = item
        self.setWindowTitle("Добавление отказавшего блока/агрегата")
        self.setModal(True)
        self.setFixedSize(350, 250)
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_combo = AgregateComboBox()
        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)
        self.system_combo.currentTextChanged.connect(self.agregate_combo.set_filter)
        self.agregate_number = QLineEdit()
        self.remove_checkbox = QCheckBox()
        self.desc = QLineEdit()
        self.button_box = QDialogButtonBox()
        self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_button = self.button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        self.save_button.clicked.connect(self.edit_create_item) # type: ignore
        self.cancel_button.clicked.connect(self.reject) # type: ignore

        form_layout = QFormLayout()
        form_layout.addRow("Группа обслуживания:", self.group_combo)
        form_layout.addRow("Система самолета:", self.system_combo)
        form_layout.addRow("Агрегат/блок:", self.agregate_combo)
        form_layout.addRow("Номер блока/агрегата:", self.agregate_number)
        form_layout.addRow("Агрегат снят?", self.remove_checkbox)
        form_layout.addRow("Примечание:", self.desc)
        
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)
        if item:
            self.load_data()

    def load_data(self):
        self.setWindowTitle("Редактирование отказавшего блока/агрегата")
        self.group_combo.setCurrentText(self.item.agregate.system.group.name)
        self.system_combo.setCurrentText(self.item.agregate.system.name)
        self.agregate_combo.setCurrentText(self.item.agregate.name)
        self.agregate_number.setText(str(self.item.number))
        self.remove_checkbox.setChecked(self.item.removed) # type: ignore
        self.desc.setText(str(self.item.description))
        
    def edit_create_item(self):
        if self.item:
            try:
                item = self.item
                item.agregate = self.agregate_combo.currentData()
                item.plane=self.plane.id
                item.number = self.agregate_number.text() # type: ignore
                item.removed = self.remove_checkbox.isChecked() # type: ignore
                item.description = self.desc.text() # type: ignore
                item.save()
                self.accept()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось изменить агрегат/блок: {str(e)}")
        else:
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
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QFormLayout, QLineEdit

from custom_components.tables import PlaneTypesTable, PlanesTypesModel, PodrazdTable, PodrazdModel, SpecTable, \
    SpecModel, GroupTable, GroupModel
from data.models import PlaneTypeBase


class UnDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.btn_ok = QPushButton('OK')
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add = QPushButton('Добавить')
        self.btn_add.clicked.connect(self.add_item)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_add)
        self.main_layout.addLayout(self.button_layout)

    def add_item(self):
        pass

class SettingsPlaneType(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self._table = PlaneTypesTable(self)
        self._model = PlanesTypesModel(self)
        self._table.setModel(self._model)
        self._model.load_data()
        self.main_layout.insertWidget(0, self._table)

    def add_item(self):
        dialog = AddPlaneType()
        dialog.exec()
        self._model.load_data()

    def refresh_data(self):
        self._model.load_data()

class SettingsPodrazd(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self._table = PodrazdTable(self)
        self._model = PodrazdModel(self)
        self._table.setModel(self._model)
        self._model.load_data()
        self.main_layout.insertWidget(0, self._table)

class SettingsSpec(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self._table = SpecTable(self)
        self._model = SpecModel(self)
        self._table.setModel(self._model)
        self._model.load_data()
        self.main_layout.insertWidget(0, self._table)

class SettingsGroup(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")
        self._table = GroupTable(self)
        self._model = GroupModel(self)
        self._table.setModel(self._model)
        self._model.load_data()
        self.main_layout.insertWidget(0, self._table)

class UnAddEditDialog(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data
        self.setModal(True)
        self.setFixedWidth(400)
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.button_layout = QHBoxLayout()

        if self._data:
            self.btn_ok = QPushButton('Сохранить')
        else:
            self.btn_ok = QPushButton('Добавить')

        self.btn_ok.clicked.connect(self.add_item)
        self.btn_cancel = QPushButton('Отменить')
        self.btn_cancel.clicked.connect(self.reject)
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_cancel)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def add_item(self):
        pass
    def config_ui(self):
        pass

class AddPlaneType(UnAddEditDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(data, parent)
        if self._data:
            self.item = PlaneTypeBase.get_by_id(data)
        self.plane_type = QLineEdit()
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle('Тип самолета')
        self.form_layout.addRow('Тип самолета:', self.plane_type)
        if self._data:
            self.plane_type.setText(self.item.name)

    def add_item(self):
        if self._data:
            self.item.name = self.plane_type.text()
            self.item.save()
            self.accept()
        PlaneTypeBase.create(name=self.plane_type.text())
        self.accept()

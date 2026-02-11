from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QFormLayout, QLineEdit, QComboBox

from custom_components.combo_box import PlaneTypeComboBox, SystemComboBox, GroupComboBox
from custom_components.tables_models import PlanesTypesModel, PodrazdModel, GroupModel, AgregateModel
from custom_components.tables import PlaneTypesTable, PodrazdTable, \
     GroupTable, AgregateTable
from data.data import TypeBase, PodrazdBase, GroupBase, AgregateBase, SystemBase


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

    def add_item(self):
        dialog = AddPodrazd()
        dialog.exec()
        self._model.load_data()

    def refresh_data(self):
        self._model.load_data()


class SettingsGroup(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")
        self._table = GroupTable(self)
        self._model = GroupModel(self)
        self._table.setModel(self._model)
        self._model.load_data()
        self.main_layout.insertWidget(0, self._table)

    def add_item(self):
        dialog = AddGroup()
        dialog.exec()
        self._model.load_data()

    def refresh_data(self):
        self._model.load_data()


class SettingsAgregate(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Блоки/Агрегаты")
        self._table = AgregateTable(self)
        self._model = AgregateModel(self)
        self._table.setModel(self._model)
        self._model.load_data()
        self.plane_type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()

        self.plane_type_combo.currentTextChanged.connect(
            lambda x: self.group_combo.set_filter(GroupBase
                                                 .select()
                                                 .where(GroupBase.plane_type == self.plane_type_combo.currentData())
                                                 )
        )
        self.plane_type_combo.currentTextChanged.connect(
            lambda x: self._model.load_data(filter_type=self.plane_type_combo.currentData())
        )
        self.group_combo.currentTextChanged.connect(
            lambda x: self.system_combo.load_data(self.group_combo.currentData())
        )
        self.group_combo.currentTextChanged.connect(
            lambda x: self._model.load_data(filter_group=self.group_combo.currentData())
        )
        self.system_combo.currentTextChanged.connect(
            lambda x: self._model.load_data(filter_system=self.system_combo.currentData())
        )
        self.main_layout.insertWidget(0, self.plane_type_combo)
        self.main_layout.insertWidget(1, self.group_combo)
        self.main_layout.insertWidget(2, self.system_combo)
        self.main_layout.insertWidget(3, self._table)

    def add_item(self):
        if self.system_combo.currentData():
            system = self.system_combo.currentData()
            dialog = AddAgregate(system=system)
        elif self.group_combo.currentData():
            group = self.group_combo.currentData()
            dialog = AddAgregate(group=group)
        elif self.plane_type_combo.currentData():
            plane_type = self.plane_type_combo.currentData()
            dialog = AddAgregate(plane_type=plane_type)
        else:
            dialog = AddAgregate()
        dialog.exec()
        self.plane_type_combo.setCurrentText(dialog.type_combo.currentText())
        self.group_combo.setCurrentText(dialog.group_combo.currentText())
        self.system_combo.setCurrentText(dialog.system_combo.currentText())

        self._model.load_data(filter_system=self.system_combo.currentData())
        # self._model.load_data()


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
            self.item = TypeBase.get_by_id(data)
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
        else:
            TypeBase.create(name=self.plane_type.text())
            self.accept()


class AddPodrazd(UnAddEditDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(data, parent)
        if self._data:
            self.item = PodrazdBase.get_by_id(data)
        self.podrazd = QLineEdit()
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle('Подразделение')
        self.form_layout.addRow('Название подразделения:', self.podrazd)
        if self._data:
            self.podrazd.setText(self.item.name)

    def add_item(self):
        if self._data:
            self.item.name = self.podrazd.text()
            self.item.save()
            self.accept()
        else:
            PodrazdBase.create(name=self.podrazd.text())
            self.accept()


class AddGroup(UnAddEditDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(data, parent)
        self.type_combo = PlaneTypeComboBox()
        self.group = QLineEdit()
        if self._data:
            self.item = GroupBase.get_by_id(data)
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle("Группы обслуживания")
        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow('Название группы', self.group)
        if self._data:
            self.group.setText(self.item.name)
            self.type_combo.setCurrentText(self.item.plane_type.name)

    def add_item(self):
        if self._data:
            self.item.name = self.group.text()
            self.item.plane_type = self.type_combo.currentData()
            self.item.save()
            self.accept()
        else:
            GroupBase.create(name=self.group.text(), plane_type=self.type_combo.currentData())
            self.accept()


class AddAgregate(UnAddEditDialog):
    def __init__(self, data=None, plane_type=None, group=None, system=None, parent=None):
        super().__init__(data, parent)
        self.type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_name = QLineEdit()

        self.type_combo.currentTextChanged.connect(
            lambda x: self.group_combo.load_data(self.type_combo.currentData())
        )
        self.group_combo.currentTextChanged.connect(
            lambda x: self.system_combo.load_data(self.group_combo.currentData())
        )

        if system:
            self.type_combo.setCurrentText(SystemBase.get_by_id(system).group.plane_type.name)
            self.group_combo.setCurrentText(SystemBase.get_by_id(system).group.name)
            self.system_combo.setCurrentText(SystemBase.get_by_id(system).name)
        elif group:
            self.type_combo.setCurrentText(GroupBase.get_by_id(group).plane_type.name)
            self.group_combo.setCurrentText(GroupBase.get_by_id(group).name)
        elif plane_type:
            self.type_combo.setCurrentText(TypeBase.get_by_id(plane_type).name)

        if self._data:
            self.item = AgregateBase.get_by_id(data)
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle("Агрегат/Блок")
        self.form_layout.addRow("Тип самолета:", self.type_combo)
        self.form_layout.addRow("Группа обслуживания:", self.group_combo)
        self.form_layout.addRow("Система самолета:", self.system_combo)
        self.form_layout.addRow('Название блока/агрегата:', self.agregate_name)

        if self._data:
            self.type_combo.setCurrentText(item.system.group.plane_type.name)
            self.group_combo.setCurrentText(item.system.group.name)
            self.system_combo.setCurrentText(item.system.name)
            self.agregate_name.setText(item.name)

    def add_item(self):
        if self._data:
            self.item.system = self.system_combo.currentData()
            self.item.name = self.agregate_name.text()
            self.item.save()
            self.accept()
        else:
            AgregateBase.create(name=self.agregate_name.text(), system=self.system_combo.currentData())
            self.accept()

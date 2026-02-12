from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QFormLayout, QLineEdit

from custom_components.combo_box import PlaneTypeComboBox, SystemComboBox, GroupComboBox
from custom_components.tables_models import PlanesTypesModel, PodrazdModel, GroupModel, AgregateModel, PlanesModel, \
    UnTableModel
from custom_components.tables import PlaneTypesTable, PodrazdTable, \
    GroupTable, AgregateTable, UnTableView
from data.data import TypeBase, PodrazdBase, GroupBase, AgregateBase, SystemBase, PlaneBase


class UnDialog(QDialog):
    updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.table = UnTableView()
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

    def refresh_data(self):
        self.table.table_model.load_data()


class SettingsPlaneType(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self.table = PlaneTypesTable(self)
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)

    def add_item(self):
        dialog = AddPlaneType()
        if dialog.exec():
            self.updated.emit()
            self.refresh_data()

    def edit_item(self, item_id):
        dialog = AddPlaneType(data=item_id)
        if dialog.exec():
            self.refresh_data()

    def delete_item(self, item_id):
        item = TypeBase.get_by_id(item_id)
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.refresh_data()


class SettingsPodrazd(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.table = PodrazdTable()
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)

    def add_item(self):
        dialog = AddPodrazd()
        if dialog.exec():
            self.updated.emit()
        self._model.load_data()

    def edit_item(self, item_id):
        dialog = AddPodrazd(data=item_id)
        if dialog.exec():
            self.refresh_data()

    def delete_item(self, item_id):
        item = PodrazdBase.get_by_id(item_id)
        self.table.table_model.delete_item(item)
        self.refresh_data()


class SettingsGroup(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")
        self.table = GroupTable(self)
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)

    def add_item(self):
        dialog = AddGroup()
        if dialog.exec():
            self.updated.emit()
            self._model.load_data()

    def edit_item(self, item_id):
        dialog = AddGroup(data=item_id)
        if dialog.exec():
            self.refresh_data()

    def delete_item(self, item_id):
        item = GroupBase.get_by_id(item_id)
        self.table.table_model.delete_item(item)
        self.refresh_data()


class SettingsAgregate(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Блоки/Агрегаты")
        self.table = AgregateTable()
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.plane_type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()

        self.plane_type_combo.currentTextChanged.connect(self.group_combo.set_filter)
        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)
        self.system_combo.currentTextChanged.connect(
            lambda x: self.table.table_model.load_data(filter_system=self.system_combo.currentData())
        )
        self.main_layout.insertWidget(0, self.plane_type_combo)
        self.main_layout.insertWidget(1, self.group_combo)
        self.main_layout.insertWidget(2, self.system_combo)
        self.main_layout.insertWidget(3, self.table)

    def edit_item(self, item_id):
        dialog = AddAgregate(data=item_id)
        if dialog.exec():
            self.update_data(dialog)

    def delete_item(self, item_id):
        item = AgregateBase.get_by_id(item_id)
        self.table.table_model.delete_item(item)
        self.refresh_data()

    def update_data(self, dialog):
        self.plane_type_combo.setCurrentText(dialog.type_combo.currentText())
        self.group_combo.setCurrentText(dialog.group_combo.currentText())
        self.system_combo.setCurrentText(dialog.system_combo.currentText())
        self._model.load_data(filter_system=self.system_combo.currentData())

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

        if dialog.exec():
            self.update_data(dialog)

        # self._model.load_data()

    def refresh_data(self):
        self.table.table_model.load_data()


class SettingsPlanes(UnDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.type_combo = PlaneTypeComboBox()
        self._table = PlaneTable()
        self._model = PlanesModel()

    def config_ui(self):
        self.setWindowTitle('Список самолетов')


class UnAddEditDialog(QDialog):
    updated = pyqtSignal()

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

        self.type_combo.currentTextChanged.connect(self.group_combo.set_filter)
        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)

        if system:
            self.type_combo.setCurrentText(SystemBase.get_by_id(system).group.plane_type.name)
            self.group_combo.setCurrentText(SystemBase.get_by_id(system).group.name)
            self.system_combo.setCurrentText(SystemBase.get_by_id(system).name)
        elif group:
            self.type_combo.setCurrentText(GroupBase.get_by_id(group).plane_type.name)
            self.group_combo.setCurrentText(GroupBase.get_by_id(group).name)
        elif plane_type:
            self.type_combo.setCurrentText(TypeBase.get_by_id(plane_type).name)

        if data:
            self.item = AgregateBase.get_by_id(data)
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle("Агрегат/Блок")
        self.form_layout.addRow("Тип самолета:", self.type_combo)
        self.form_layout.addRow("Группа обслуживания:", self.group_combo)
        self.form_layout.addRow("Система самолета:", self.system_combo)
        self.form_layout.addRow('Название блока/агрегата:', self.agregate_name)

        if self._data:
            self.type_combo.setCurrentText(self.item.system.group.plane_type.name)
            self.group_combo.setCurrentText(self.item.system.group.name)
            self.system_combo.setCurrentText(self.item.system.name)
            self.agregate_name.setText(self.item.name)

    def add_item(self):
        if self._data:
            self.item.system = self.system_combo.currentData()
            self.item.name = self.agregate_name.text()
            self.item.save()
            self.accept()
        else:
            AgregateBase.create(name=self.agregate_name.text(), system=self.system_combo.currentData())
            self.accept()


class AddPlane(UnAddEditDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(data, parent)
        self.type_combo = PlaneTypeComboBox()
        self.bort_num = QLineEdit()
        self.zav_num = QLineEdit()

        if self._data:
            self.item = PlaneBase.get_by_id(data)
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle("Добавить самолет")
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

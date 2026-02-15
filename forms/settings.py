from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QFormLayout, QLineEdit

from custom_components.combo_box import PlaneTypeComboBox, SystemComboBox, GroupComboBox, PodrazdComboBox

from custom_components.tables import PlaneTypesTable, PodrazdTable, \
    GroupTable, AgregateTable, UnTableView, PlanesTable, OsobTable
from custom_components.tables_models import OsobModel
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

    def edit_item(self, item_id):
        pass

    def delete_item(self, item_id):
        pass

    def refresh_data(self, **kwargs):
        self.table.table_model.load_data(**kwargs)


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
        dialog.updated.connect(self.refresh_data)
        dialog.add_dialog()

    def edit_item(self, item):
        dialog = AddPlaneType()
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
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
        dialog.updated.connect(self.refresh_data)
        dialog.add_dialog()
        self.updated.emit()

    def edit_item(self, item_id):
        dialog = AddPodrazd()
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item_id)
        self.updated.emit()

    def delete_item(self, item_id):
        item = PodrazdBase.get_by_id(item_id)
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsGroup(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")
        self.type_combo = PlaneTypeComboBox()
        self.table = GroupTable(self)
        self.type_combo.currentTextChanged.connect(self.table.set_filter)
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.type_combo)
        self.main_layout.insertWidget(1, self.table)

    def add_item(self):
        dialog = AddGroup()
        dialog.updated.connect(self.refresh_data)
        dialog.add_dialog()

    def edit_item(self, item_id):
        dialog = AddGroup()
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item_id)

    def delete_item(self, item_id):
        self.table.table_model.delete_item(item_id)
        self.refresh_data()


class SettingsAgregate(UnDialog):
    add_signal = pyqtSignal(object, object, object)

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
        self.plane_type_combo.currentTextChanged.connect(
            lambda x: self.table.table_model.load_data(filter_type=self.plane_type_combo.currentData())
        )

        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)
        self.group_combo.currentTextChanged.connect(
            lambda x: self.table.table_model.load_data(filter_group=self.group_combo.currentData())
        )

        self.system_combo.currentTextChanged.connect(
            lambda x: self.table.table_model.load_data(filter_system=self.system_combo.currentData())
        )
        self.main_layout.insertWidget(0, self.plane_type_combo)
        self.main_layout.insertWidget(1, self.group_combo)
        self.main_layout.insertWidget(2, self.system_combo)
        self.main_layout.insertWidget(3, self.table)

    def edit_item(self, item):
        dialog = AddAgregate()
        dialog.edit_dialog(item)
        if dialog.exec():
            self.update_from_dialog(dialog)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data()

    def add_item(self):
        dialog = AddAgregate()
        dialog.add_dialog(self.plane_type_combo.currentData(Qt.ItemDataRole.UserRole),
                          self.group_combo.currentData(Qt.ItemDataRole.UserRole),
                          self.system_combo.currentData(Qt.ItemDataRole.UserRole))

        if dialog.exec():
            self.update_from_dialog(dialog)

    def update_from_dialog(self, dialog):
        self.plane_type_combo.setCurrentText(dialog.type_combo.currentText())
        self.group_combo.setCurrentText(dialog.group_combo.currentText())
        self.system_combo.setCurrentText(dialog.system_combo.currentText())
        self.refresh_data(filter_type=dialog.type_combo.currentData(),
                          filter_group=dialog.group_combo.currentData(),
                          filter_system=dialog.system_combo.currentData())


class SettingsPlanes(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Самолеты")
        self.table = PlanesTable()
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)

    def add_item(self):
        dialog = AddPlane()
        dialog.updated.connect(self.refresh_data)
        dialog.add_dialog()

    def edit_item(self, item):
        dialog = AddPlane()
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data()


class SettingsOsob(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Особенности самолетов')
        self.table = OsobTable()
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)

    def add_item(self):
        dialog = AddOsob()
        if dialog.exec():
            self.refresh_data()

    def edit_item(self, item):
        dialog = AddOsob()
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item)
        if dialog.exec():
            self.refresh_data()

    def delete_item(self, item_id):
        self.table.table_model.delete_item(item_id)
        self.refresh_data()


class UnAddEditDialog(QDialog):
    updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.item = None
        self.setModal(True)
        self.setFixedWidth(400)
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.button_layout = QHBoxLayout()
        self.btn_ok = QPushButton('Добавить')

        self.btn_ok.clicked.connect(self.add_or_save_item)
        self.btn_cancel = QPushButton('Отменить')
        self.btn_cancel.clicked.connect(self.reject)
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_cancel)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def add_or_save_item(self):
        pass

    def add_dialog(self, *args):
        pass

    def edit_dialog(self, item_id):
        pass


class AddPlaneType(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plane_type = QLineEdit()
        self.config_ui()

    def add_dialog(self):
        if self.exec():
            self.updated.emit()

    def edit_dialog(self, item):
        self.item = item
        self.plane_type.setText(self.item.name)
        self.btn_ok.setText('Сохранить')
        if self.exec():
            self.updated.emit()

    def config_ui(self):
        self.setWindowTitle('Добавить тип самолета')
        self.form_layout.addRow('Тип самолета:', self.plane_type)

    def add_or_save_item(self):
        if self.item:
            self.item.name = self.plane_type.text()
            self.item.save()
            self.updated.emit()
            self.accept()
        else:
            TypeBase.create(name=self.plane_type.text())
            self.updated.emit()
            self.accept()


class AddPodrazd(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.podrazd = QLineEdit()
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle('Подразделение')
        self.form_layout.addRow('Название подразделения:', self.podrazd)

    def add_dialog(self):
        if self.exec():
            self.updated.emit()

    def edit_dialog(self, item):
        self.item = item
        self.podrazd.setText(self.item.name)
        self.btn_ok.setText('Сохранить')
        if self.exec():
            self.updated.emit()

    def add_or_save_item(self):
        if self.item:
            self.item.name = self.podrazd.text()
            self.item.save()
            self.updated.emit()
            self.accept()
        else:
            PodrazdBase.create(name=self.podrazd.text())
            self.updated.emit()
            self.accept()


class AddGroup(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_combo = PlaneTypeComboBox()
        self.group = QLineEdit()
        self.config_ui()

    def add_dialog(self):
        if self.exec():
            self.updated.emit()

    def edit_dialog(self, item):
        self.item = item
        self.type_combo.setCurrentText(self.item.plane_type.name)
        self.group.setText(self.item.name)
        self.btn_ok.setText('Сохранить')
        if self.exec():
            self.updated.emit()

    def config_ui(self):
        self.setWindowTitle("Группы обслуживания")
        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow('Название группы', self.group)

    def add_or_save_item(self):
        if self.item:
            self.item.name = self.group.text()
            self.item.plane_type = self.type_combo.currentData()
            self.item.save()
            self.accept()
        else:
            GroupBase.create(name=self.group.text(), plane_type=self.type_combo.currentData())
            self.accept()


class AddAgregate(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_name = QLineEdit()

        self.group_combo.setDisabled(True)
        self.system_combo.setDisabled(True)
        self.agregate_name.setDisabled(True)
        self.btn_ok.setDisabled(True)

        self.type_combo.currentTextChanged.connect(self.group_combo.set_filter)
        self.type_combo.currentTextChanged.connect(self.check)
        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)
        self.group_combo.currentTextChanged.connect(self.check)
        self.system_combo.currentTextChanged.connect(self.check)

        self.config_ui()

    def check(self):
        plane_type = isinstance(self.type_combo.currentData(role=Qt.ItemDataRole.UserRole), TypeBase)
        group = isinstance(self.group_combo.currentData(role=Qt.ItemDataRole.UserRole), GroupBase)
        system = isinstance(self.system_combo.currentData(role=Qt.ItemDataRole.UserRole), SystemBase)
        if plane_type:
            self.group_combo.setEnabled(True)
            if group:
                self.system_combo.setEnabled(True)
                if system:
                    self.agregate_name.setEnabled(True)
                    self.btn_ok.setEnabled(True)
                else:
                    self.agregate_name.setDisabled(True)
                    self.btn_ok.setEnabled(False)
            else:
                self.system_combo.setEnabled(False)
                self.agregate_name.setEnabled(False)
                self.btn_ok.setEnabled(False)
        else:
            self.group_combo.setEnabled(False)
            self.system_combo.setEnabled(False)
            self.agregate_name.setEnabled(False)
            self.btn_ok.setEnabled(False)

    def add_dialog(self, plane_type: TypeBaseBase, group: GroupBase, system: SystemBase):
        if isinstance(plane_type, TypeBase):
            self.type_combo.setCurrentText(plane_type.name)
            if isinstance(group, GroupBase):
                self.group_combo.setCurrentText(group.name)
                if isinstance(system, SystemBase):
                    self.system_combo.setCurrentText(system.name)

    def edit_dialog(self, item):
        self.item = item
        self.type_combo.setCurrentText(self.item.system.group.plane_type.name)
        self.group_combo.setCurrentText(self.item.system.group.name)
        self.system_combo.setCurrentText(self.item.system.name)
        self.agregate_name.setText(self.item.name)

    def config_ui(self):
        self.setWindowTitle("Агрегат/Блок")
        self.form_layout.addRow("Тип самолета:", self.type_combo)
        self.form_layout.addRow("Группа обслуживания:", self.group_combo)
        self.form_layout.addRow("Система самолета:", self.system_combo)
        self.form_layout.addRow('Название блока/агрегата:', self.agregate_name)

    def add_or_save_item(self):
        if self.item:
            self.item.system = self.system_combo.currentData()
            self.item.name = self.agregate_name.text()
            self.item.save()
            self.accept()
        else:
            AgregateBase.create(name=self.agregate_name.text(), system=self.system_combo.currentData())
            self.accept()


class AddPlane(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_combo = PlaneTypeComboBox()
        self.podrazd = PodrazdComboBox()
        self.bort_number = QLineEdit()
        self.zav_num = QLineEdit()
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle("Добавить самолет")
        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow('Подразделение:', self.podrazd)
        self.form_layout.addRow('Бортовой номер:', self.bort_number)
        self.form_layout.addRow('Заводской номер:', self.zav_num)

    def add_dialog(self):
        if self.exec():
            self.updated.emit()

    def edit_dialog(self, item):
        self.setWindowTitle('Редактировать самолет')
        self.btn_ok.setText('Сохранить')
        self.item = item
        self.type_combo.setCurrentText(self.item.plane_type.name)
        self.podrazd.setCurrentText(self.item.podrazd.name)
        self.bort_number.setText(self.item.bort_number)
        self.zav_num.setText(self.item.zav_num)
        if self.exec():
            self.updated.emit()

    def add_or_save_item(self):
        if self.item:
            self.item.plane_type = self.type_combo.currentData()
            self.item.podrazd = self.podrazd.currentData()
            self.item.bort_number = self.bort_number.text()
            self.item.zav_num = self.zav_num.text()
            self.item.save()
            self.accept()
        else:
            PlaneBase.create(plane_type=self.type_combo.currentData(),
                             podrazd=self.podrazd.currentData(),
                             bort_number=self.bort_number.text(),
                             zav_num=self.zav_num.text())
            self.accept()


class AddOsob(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_combo = PlaneTypeComboBox()
        self.osob = QLineEdit()
        self.config_ui()

    def config_ui(self):
        self.setWindowTitle("Добавить особенность")
        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow('Особенность:', self.osob)

    def edit_item(self, item_id):
        self.setWindowTitle('Редактировать особенность')
        self.item = OsobModel.get_by_id(item_id)
        self.type_combo.setCurrentText(self.item.plane_type.name)
        self.osob.setText(self.item.name)

    def add_or_save_item(self):
        if self.item:
            self.item.plane_type = self.type_combo.currentData()
            self.item.podrazd = self.podrazd.currentData()
            self.item.bort_number = self.bort_number.text()
            self.item.zav_num = self.zav_num.text()
            self.item.save()
            self.accept()
        else:
            PlaneBase.create(plane_type=self.type_combo.currentData(),
                             podrazd=self.podrazd.currentData(),
                             bort_number=self.bort_number.text(),
                             zav_num=self.zav_num.text())
            self.accept()

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QHBoxLayout,
    QFormLayout, QLineEdit, QMessageBox
)

from custom_components.combo_box import (
    PlaneTypeComboBox, SystemComboBox, GroupComboBox, PodrazdComboBox
)
from custom_components.tables import (
    PlaneTypesTable, PodrazdTable, GroupTable,
    AgregateTable, PlanesTable
)
from data.data import (
    TypeBase, PodrazdBase, GroupBase, AgregateBase,
    SystemBase, PlaneBase
)


# ----------------------------------------------------------------------
# Базовые классы
# ----------------------------------------------------------------------
class UnDialog(QDialog):
    """Базовый диалог для просмотра и редактирования справочников."""
    updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Кнопки
        self.btn_ok = QPushButton('OK')
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add = QPushButton('Добавить')
        self.btn_add.clicked.connect(self.add_item)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_add)

    def setup_ui(self, table_class, table_kwargs=None):
        """Инициализация таблицы и подключение сигналов."""
        self.table = table_class(**(table_kwargs or {}))
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)
        self.main_layout.addLayout(self.button_layout)

    def add_item(self):
        """Переопределяется в наследниках."""
        pass

    def edit_item(self, item):
        """Переопределяется в наследниках."""
        pass

    def delete_item(self, item):
        """Переопределяется в наследниках."""
        pass

    def refresh_data(self, **kwargs):
        """Обновление данных таблицы."""
        if hasattr(self.table, 'table_model'):
            self.table.table_model.load_data(**kwargs)

    def handle_crud_dialog(self, dialog_class, method='add', item=None, **dialog_kwargs):
        """
        Общий метод для открытия диалогов добавления/редактирования.
        """
        dialog = dialog_class(self)
        if hasattr(dialog, 'updated'):
            dialog.updated.connect(self.refresh_data)

        if method == 'add':
            dialog.add_dialog(**dialog_kwargs)
        else:  # edit
            dialog.edit_dialog(item)

        if dialog.exec():
            self.updated.emit()
            return dialog
        return None


class FilteredSettingsDialog(UnDialog):
    """Базовый класс для диалогов с фильтрацией (добавляет фильтры сверху)."""

    def setup_filters(self, filter_widgets):
        """Размещение виджетов фильтрации перед таблицей."""
        for widget in filter_widgets:
            self.main_layout.insertWidget(self.main_layout.count() - 1, widget)


# ----------------------------------------------------------------------
# Базовый класс для диалогов добавления/редактирования записи
# ----------------------------------------------------------------------
class UnAddEditDialog(QDialog):
    """Базовый диалог для добавления/редактирования элемента справочника."""
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
        """Должен быть переопределён в наследниках."""
        raise NotImplementedError

    def add_dialog(self, **kwargs):
        """Вызывается при открытии в режиме добавления (может принимать параметры)."""
        pass

    def edit_dialog(self, item):
        """Вызывается при открытии в режиме редактирования."""
        self.item = item
        self.btn_ok.setText('Сохранить')

    def show_error(self, message):
        """Показать сообщение об ошибке."""
        QMessageBox.warning(self, "Ошибка", message)


# ----------------------------------------------------------------------
# Миксин для диалогов с одним текстовым полем (имя/название)
# ----------------------------------------------------------------------
class SingleFieldMixin:
    """Миксин для диалогов, содержащих только одно поле ввода."""

    def __init__(self, field_label, parent=None):
        # Сохраняем label для последующего использования
        self.field_label = field_label
        # Важно: вызываем super() без parent, т.к. parent уже передан в конструкторе
        super().__init__(parent)

    def init_field(self):
        """Инициализация поля ввода (должен вызываться после super().__init__)."""
        self.field_edit = QLineEdit()
        self.form_layout.addRow(self.field_label, self.field_edit)

    def set_field_text(self, text):
        self.field_edit.setText(text)

    def get_field_text(self):
        return self.field_edit.text().strip()


# ----------------------------------------------------------------------
# Конкретные диалоги настроек (справочников)
# ----------------------------------------------------------------------
class SettingsPlaneType(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self.setup_ui(PlaneTypesTable)

    def add_item(self):
        self.handle_crud_dialog(AddPlaneType, 'add')

    def edit_item(self, item):
        self.handle_crud_dialog(AddPlaneType, 'edit', item)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsPodrazd(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.setup_ui(PodrazdTable)

    def add_item(self):
        self.handle_crud_dialog(AddPodrazd, 'add')

    def edit_item(self, item):
        self.handle_crud_dialog(AddPodrazd, 'edit', item)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsGroup(FilteredSettingsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")

        # Фильтр по типу самолёта
        self.type_combo = PlaneTypeComboBox()
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.setup_filters([self.type_combo])

        # Таблица
        self.setup_ui(GroupTable, {'parent': self})

    def on_type_changed(self, text):
        if hasattr(self.table, 'set_filter'):
            self.table.set_filter(text)

    def add_item(self):
        # Передаём выбранный тип в диалог добавления
        selected_type = self.type_combo.currentData()
        self.handle_crud_dialog(
            AddGroup, 'add',
            plane_type=selected_type if selected_type else None
        )

    def edit_item(self, item):
        self.handle_crud_dialog(AddGroup, 'edit', item)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsAgregate(FilteredSettingsDialog):
    add_signal = pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Блоки/Агрегаты")

        # Фильтры
        self.plane_type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()

        # Связи
        self.plane_type_combo.currentTextChanged.connect(self.on_plane_type_changed)
        self.group_combo.currentTextChanged.connect(self.on_group_changed)
        self.system_combo.currentTextChanged.connect(self.on_system_changed)

        # Размещаем фильтры сверху
        self.setup_filters([self.plane_type_combo, self.group_combo, self.system_combo])

        # Таблица
        self.setup_ui(AgregateTable)

    def get_filter_params(self):
        """Возвращает текущие выбранные объекты фильтров."""
        return {
            'filter_type': self.plane_type_combo.currentData(),
            'filter_group': self.group_combo.currentData(),
            'filter_system': self.system_combo.currentData()
        }

    def on_plane_type_changed(self, text):
        self.group_combo.set_filter(text)
        self.refresh_data(**self.get_filter_params())

    def on_group_changed(self, text):
        self.system_combo.set_filter(text)
        self.refresh_data(**self.get_filter_params())

    def on_system_changed(self, text):
        self.refresh_data(**self.get_filter_params())

    def add_item(self):
        filters = self.get_filter_params()
        dialog = AddAgregate(self)
        dialog.updated.connect(self.refresh_data)
        dialog.add_dialog(**filters)
        if dialog.exec():
            self.update_after_dialog(dialog)

    def edit_item(self, item):
        dialog = AddAgregate(self)
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item)
        if dialog.exec():
            self.update_after_dialog(dialog)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data(**self.get_filter_params())
        self.updated.emit()

    def update_after_dialog(self, dialog):
        """Синхронизирует фильтры с диалогом и обновляет таблицу."""
        self.plane_type_combo.setCurrentText(dialog.type_combo.currentText())
        self.group_combo.setCurrentText(dialog.group_combo.currentText())
        self.system_combo.setCurrentText(dialog.system_combo.currentText())
        self.refresh_data(**self.get_filter_params())


class SettingsPlanes(UnDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Самолеты")
        self.setup_ui(PlanesTable)

    def add_item(self):
        self.handle_crud_dialog(AddPlane, 'add')

    def edit_item(self, item):
        self.handle_crud_dialog(AddPlane, 'edit', item)

    def delete_item(self, item):
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


# ----------------------------------------------------------------------
# Диалоги добавления/редактирования элементов
# ----------------------------------------------------------------------
class AddPlaneType(SingleFieldMixin, UnAddEditDialog):
    """Диалог добавления/редактирования типа самолета."""

    def __init__(self, parent=None):
        # Сначала вызываем SingleFieldMixin с его аргументом field_label
        SingleFieldMixin.__init__(self, "Тип самолета:", parent)
        # UnAddEditDialog.__init__ вызывается через super() в SingleFieldMixin
        self.init_field()
        self.setWindowTitle('Добавить тип самолета')

    def edit_dialog(self, item):
        super().edit_dialog(item)
        self.set_field_text(item.name)

    def add_or_save_item(self):
        name = self.get_field_text()
        if not name:
            self.show_error("Название не может быть пустым")
            return

        if self.item:
            self.item.name = name
            self.item.save()
        else:
            TypeBase.create(name=name)

        self.updated.emit()
        self.accept()


class AddPodrazd(SingleFieldMixin, UnAddEditDialog):
    """Диалог добавления/редактирования подразделения."""

    def __init__(self, parent=None):
        SingleFieldMixin.__init__(self, "Название подразделения:", parent)
        self.init_field()
        self.setWindowTitle('Подразделение')

    def edit_dialog(self, item):
        super().edit_dialog(item)
        self.set_field_text(item.name)

    def add_or_save_item(self):
        name = self.get_field_text()
        if not name:
            self.show_error("Название не может быть пустым")
            return

        if self.item:
            self.item.name = name
            self.item.save()
        else:
            PodrazdBase.create(name=name)

        self.updated.emit()
        self.accept()


class AddGroup(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")

        self.type_combo = PlaneTypeComboBox()
        self.group_edit = QLineEdit()

        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow('Название группы', self.group_edit)

    def add_dialog(self, plane_type=None):
        if plane_type and isinstance(plane_type, TypeBase):
            self.type_combo.setCurrentText(plane_type.name)

    def edit_dialog(self, item):
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.group_edit.setText(item.name)

    def add_or_save_item(self):
        name = self.group_edit.text().strip()
        plane_type = self.type_combo.currentData()

        if not name:
            self.show_error("Название группы не может быть пустым")
            return

        if plane_type is None:
            self.show_error("Выберите тип самолета")
            return

        if self.item:
            self.item.name = name
            self.item.plane_type = plane_type
            self.item.save()
        else:
            GroupBase.create(name=name, plane_type=plane_type)

        self.updated.emit()
        self.accept()


class AddAgregate(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Агрегат/Блок")

        self.type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_edit = QLineEdit()

        # Изначально все, кроме типа, отключены
        self.group_combo.setEnabled(False)
        self.system_combo.setEnabled(False)
        self.agregate_edit.setEnabled(False)
        self.btn_ok.setEnabled(False)

        # Подключаем сигналы для поэтапного включения
        self.type_combo.currentIndexChanged.connect(self.update_state)
        self.group_combo.currentIndexChanged.connect(self.update_state)
        self.system_combo.currentIndexChanged.connect(self.update_state)
        self.agregate_edit.textChanged.connect(self.update_state)

        # Привязываем фильтрацию дочерних комбобоксов
        self.type_combo.currentTextChanged.connect(self.group_combo.set_filter)
        self.group_combo.currentTextChanged.connect(self.system_combo.set_filter)

        # Добавляем поля в форму
        self.form_layout.addRow("Тип самолета:", self.type_combo)
        self.form_layout.addRow("Группа обслуживания:", self.group_combo)
        self.form_layout.addRow("Система самолета:", self.system_combo)
        self.form_layout.addRow('Название блока/агрегата:', self.agregate_edit)

    def update_state(self):
        """Включает/выключает поля в зависимости от выбранных значений."""
        type_selected = self.type_combo.currentData() is not None
        group_selected = self.group_combo.currentData() is not None
        system_selected = self.system_combo.currentData() is not None
        name_filled = bool(self.agregate_edit.text().strip())

        self.group_combo.setEnabled(type_selected)
        self.system_combo.setEnabled(type_selected and group_selected)
        self.agregate_edit.setEnabled(type_selected and group_selected and system_selected)
        self.btn_ok.setEnabled(type_selected and group_selected and system_selected and name_filled)

    def add_dialog(self, filter_type=None, filter_group=None, filter_system=None):
        """Предустановка фильтров из родительского диалога."""
        if isinstance(filter_type, TypeBase):
            self.type_combo.setCurrentText(filter_type.name)
        if isinstance(filter_group, GroupBase):
            self.group_combo.setCurrentText(filter_group.name)
        if isinstance(filter_system, SystemBase):
            self.system_combo.setCurrentText(filter_system.name)

    def edit_dialog(self, item):
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.system.group.plane_type.name)
        self.group_combo.setCurrentText(item.system.group.name)
        self.system_combo.setCurrentText(item.system.name)
        self.agregate_edit.setText(item.name)

    def add_or_save_item(self):
        name = self.agregate_edit.text().strip()
        system = self.system_combo.currentData()

        if not name:
            self.show_error("Название агрегата не может быть пустым")
            return

        if system is None:
            self.show_error("Выберите систему")
            return

        if self.item:
            self.item.name = name
            self.item.system = system
            self.item.save()
        else:
            AgregateBase.create(name=name, system=system)

        self.updated.emit()
        self.accept()


class AddPlane(UnAddEditDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить самолет")

        self.type_combo = PlaneTypeComboBox()
        self.podrazd_combo = PodrazdComboBox()
        self.bort_edit = QLineEdit()
        self.zav_edit = QLineEdit()

        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow('Подразделение:', self.podrazd_combo)
        self.form_layout.addRow('Бортовой номер:', self.bort_edit)
        self.form_layout.addRow('Заводской номер:', self.zav_edit)

    def edit_dialog(self, item):
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.podrazd_combo.setCurrentText(item.podrazd.name)
        self.bort_edit.setText(item.bort_number)
        self.zav_edit.setText(item.zav_num)

    def add_or_save_item(self):
        bort = self.bort_edit.text().strip()
        zav = self.zav_edit.text().strip()
        plane_type = self.type_combo.currentData()
        podrazd = self.podrazd_combo.currentData()

        if not bort:
            self.show_error("Бортовой номер не может быть пустым")
            return

        if not zav:
            self.show_error("Заводской номер не может быть пустым")
            return

        if plane_type is None:
            self.show_error("Выберите тип самолета")
            return

        if podrazd is None:
            self.show_error("Выберите подразделение")
            return

        if self.item:
            self.item.plane_type = plane_type
            self.item.podrazd = podrazd
            self.item.bort_number = bort
            self.item.zav_num = zav
            self.item.save()
        else:
            PlaneBase.create(
                plane_type=plane_type,
                podrazd=podrazd,
                bort_number=bort,
                zav_num=zav
            )

        self.updated.emit()
        self.accept()
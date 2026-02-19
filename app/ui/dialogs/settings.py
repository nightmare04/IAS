"""Settings dialogs for managing reference data."""
from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.models.aircraft import (
    AgregateBase,
    GroupBase,
    PlaneBase,
    PodrazdBase,
    SystemBase,
    TypeBase,
)
from app.ui.widgets.combo_box import (
    GroupComboBox,
    PlaneTypeComboBox,
    PodrazdComboBox,
    SystemComboBox,
)
from app.ui.widgets.tables import (
    AgregateTable,
    GroupTable,
    OsobTable,
    PlanesTable,
    PlaneTypesTable,
    PodrazdTable,
    SystemTable,
)


# ----------------------------------------------------------------------
# Base classes
# ----------------------------------------------------------------------
class UnDialog(QDialog):
    """Base dialog for viewing and editing reference data."""

    updated = pyqtSignal()

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_item)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_add)

    def setup_ui(self, table_class: type, table_kwargs: dict | None = None) -> None:
        """Initialize table and connect signals."""
        self.table = table_class(**(table_kwargs or {}))
        self.table.edit_signal.connect(self.edit_item)
        self.table.delete_signal.connect(self.delete_item)
        self.main_layout.insertWidget(0, self.table)
        self.main_layout.addLayout(self.button_layout)

    def add_item(self) -> None:
        """Override in subclasses."""
        raise NotImplementedError()

    def edit_item(self, item: Any) -> None:
        """Override in subclasses."""
        raise NotImplementedError()

    def delete_item(self, item: Any) -> None:
        """Override in subclasses."""
        raise NotImplementedError()

    def refresh_data(self, **kwargs: Any) -> None:
        """Refresh table data."""
        if hasattr(self.table, "table_model"):
            self.table.table_model.load_data(**kwargs)

    def handle_dialog(
        self, dialog_class: type, method: str = "add", item: Any | None = None, **dialog_kwargs: Any
    ) -> QDialog | None:
        """Common method for opening add/edit dialogs."""
        dialog = dialog_class(self)
        dialog.updated.connect(self.refresh_data)

        if method == "add":
            dialog.add_dialog(**dialog_kwargs)
        else:
            dialog.edit_dialog(item)

        if dialog.exec():
            self.updated.emit()
            return dialog
        return None


class UnAddEditDialog(QDialog):
    """Base dialog for adding/editing reference data items."""

    updated = pyqtSignal()

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.item: Any | None = None
        self.setModal(True)
        self.setFixedWidth(400)
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.button_layout = QHBoxLayout()

        self.btn_ok = QPushButton("Добавить")
        self.btn_ok.clicked.connect(self.add_or_save_item)
        self.btn_cancel = QPushButton("Отменить")
        self.btn_cancel.clicked.connect(self.reject)

        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_cancel)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def add_or_save_item(self) -> None:
        """Override in subclasses."""
        raise NotImplementedError

    def add_dialog(self, **kwargs: Any) -> None:
        """Called when opening in add mode."""
        pass

    def edit_dialog(self, item: Any) -> None:
        """Called when opening in edit mode."""
        self.item = item
        self.btn_ok.setText("Сохранить")

    def show_error(self, message: str) -> None:
        """Show error message."""
        QMessageBox.warning(self, "Ошибка", message)


class SingleFieldMixin:
    """Mixin for dialogs with single text input field."""

    def __init__(self, field_label: str, parent: Any | None = None) -> None:
        self.field_label = field_label
        super().__init__()

    def init_field(self) -> None:
        """Initialize text input field."""
        self.field_edit = QLineEdit()
        self.form_layout.addRow(self.field_label, self.field_edit) # type: ignore

    def set_field_text(self, text: str) -> None:
        """Set field text."""
        self.field_edit.setText(text)

    def get_field_text(self) -> str:
        """Get field text."""
        return self.field_edit.text().strip()


# ----------------------------------------------------------------------
# Settings dialogs
# ----------------------------------------------------------------------
class SettingsPlaneType(UnDialog):
    """Dialog for managing aircraft types."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self.setup_ui(PlaneTypesTable)

    def add_item(self) -> None:
        self.handle_dialog(AddPlaneType, "add")

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddPlaneType, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsPodrazd(UnDialog):
    """Dialog for managing divisions."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.setup_ui(PodrazdTable)

    def add_item(self) -> None:
        self.handle_dialog(AddPodrazd, "add")

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddPodrazd, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsGroup(UnDialog):
    """Dialog for managing maintenance groups."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")

        self.type_combo = PlaneTypeComboBox()

        self.setup_ui(GroupTable, {"parent": self})
        self.main_layout.insertWidget(0, self.type_combo)

    def add_item(self) -> None:
        selected_type = self.type_combo.currentData()
        self.handle_dialog(AddGroup, "add", plane_type=selected_type if selected_type else None)

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddGroup, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsSystem(UnDialog):
    """Dialog for managing aircraft systems."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Системы самолетов")

        self.type_combo = PlaneTypeComboBox()
        self.type_combo.changed.connect(self.on_type_changed)

        self.setup_ui(SystemTable, {"parent": self})
        self.main_layout.insertWidget(0, self.type_combo)

    def on_type_changed(self, plane_type: Any) -> None:
        """Filter table by aircraft type."""
        if plane_type:
            self.table.set_filter(plane_type.name)
        else:
            self.table.set_filter("")

    def add_item(self) -> None:
        selected_type = self.type_combo.currentData()
        self.handle_dialog(AddSystem, "add", plane_type=selected_type if selected_type else None)

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddSystem, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


class SettingsAgregate(UnDialog):
    """Dialog for managing aggregates/units."""

    add_signal = pyqtSignal(object, object, object)

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Блоки/Агрегаты")

        self.plane_type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()

        self.plane_type_combo.changed.connect(self.group_combo.set_filter)
        self.group_combo.changed.connect(self.system_combo.set_filter)

        self.plane_type_combo.currentTextChanged.connect(self.on_data_changed)
        self.system_combo.currentTextChanged.connect(self.on_data_changed)

        self.setup_ui(AgregateTable)

        self.main_layout.insertWidget(0, self.plane_type_combo)
        self.main_layout.insertWidget(1, self.group_combo)
        self.main_layout.insertWidget(2, self.system_combo)

    def get_filter_params(self) -> dict[str, Any]:
        """Get current filter parameters."""
        return {
            "filter_type": self.plane_type_combo.currentData(),
            "filter_group": self.group_combo.currentData(),
            "filter_system": self.system_combo.currentData(),
        }

    def on_data_changed(self) -> None:
        self.refresh_data(**self.get_filter_params())

    def add_item(self) -> None:
        filters = self.get_filter_params()
        dialog = AddAgregate(self)
        dialog.updated.connect(self.refresh_data)
        dialog.add_dialog(**filters)
        if dialog.exec():
            self.update_after_dialog(dialog)

    def edit_item(self, item: Any) -> None:
        dialog = AddAgregate(self)
        dialog.updated.connect(self.refresh_data)
        dialog.edit_dialog(item)
        if dialog.exec():
            self.update_after_dialog(dialog)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data(**self.get_filter_params())
        self.updated.emit()

    def update_after_dialog(self, dialog: "AddAgregate") -> None:
        """Synchronize filters with dialog and refresh table."""
        self.plane_type_combo.setCurrentText(dialog.type_combo.currentText())
        self.group_combo.setCurrentText(dialog.group_combo.currentText())
        self.system_combo.setCurrentText(dialog.system_combo.currentText())
        self.refresh_data(**self.get_filter_params())


class SettingsPlanes(UnDialog):
    """Dialog for managing aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Самолеты")
        self.setup_ui(PlanesTable)

        self.plane_type = PlaneTypeComboBox()
        self.plane_type.changed.connect(self.set_filter)
        self.podrazd = PodrazdComboBox()
        self.podrazd.changed.connect(self.set_filter)

        self.main_layout.insertWidget(0, self.plane_type)
        self.main_layout.insertWidget(1, self.podrazd)

    def set_filter(self) -> None:
        filter_dict = {
            "plane_type": self.plane_type.currentData(),
            "podrazd": self.podrazd.currentData(),
        }
        self.table.table_model.set_filter(filter_dict)

    def add_item(self) -> None:
        self.handle_dialog(AddPlane, "add")

    def edit_item(self, item: Any) -> None:
        self.handle_dialog(AddPlane, "edit", item)

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()


# ----------------------------------------------------------------------
# Add/Edit dialogs
# ----------------------------------------------------------------------
class AddPlaneType(SingleFieldMixin, UnAddEditDialog):
    """Dialog for adding/editing aircraft type."""

    def __init__(self, parent: Any | None = None) -> None:
        SingleFieldMixin.__init__(self, "Тип самолета:", parent)
        self.init_field()
        self.setWindowTitle("Добавить тип самолета")

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.set_field_text(item.name)

    def add_or_save_item(self) -> None:
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
    """Dialog for adding/editing division."""

    def __init__(self, parent: Any | None = None) -> None:
        SingleFieldMixin.__init__(self, "Название подразделения:", parent)
        self.init_field()
        self.setWindowTitle("Подразделение")

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.set_field_text(item.name)

    def add_or_save_item(self) -> None:
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
    """Dialog for adding/editing maintenance group."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Группы обслуживания")

        self.type_combo = PlaneTypeComboBox()
        self.group_edit = QLineEdit()

        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow("Название группы", self.group_edit)

    def add_dialog(self, plane_type: TypeBase | None = None) -> None:
        if plane_type and isinstance(plane_type, TypeBase):
            self.type_combo.setCurrentText(str(plane_type.name))

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.group_edit.setText(item.name)

    def add_or_save_item(self) -> None:
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


class AddSystem(UnAddEditDialog):
    """Dialog for adding/editing aircraft system."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Система самолета")

        self.type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_edit = QLineEdit()

        self.group_combo.setEnabled(False)
        self.system_edit.setEnabled(False)
        self.btn_ok.setEnabled(False)

        self.type_combo.currentIndexChanged.connect(self.update_state)
        self.group_combo.currentIndexChanged.connect(self.update_state)
        self.system_edit.textChanged.connect(self.update_state)

        self.type_combo.changed.connect(self.on_type_changed)

        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow("Группа обслуживания", self.group_combo)
        self.form_layout.addRow("Название системы", self.system_edit)

    def on_type_changed(self, plane_type: Any) -> None:
        """Update group combo filter when type changes."""
        if plane_type:
            self.group_combo.set_filter(plane_type)
            self.group_combo._model.refresh()

    def update_state(self) -> None:
        """Enable/disable fields based on selections."""
        type_selected = self.type_combo.currentData() is not None
        group_selected = self.group_combo.currentData() is not None
        name_filled = bool(self.system_edit.text().strip())

        self.group_combo.setEnabled(type_selected)
        self.system_edit.setEnabled(type_selected and group_selected)
        self.btn_ok.setEnabled(type_selected and group_selected and name_filled)

    def add_dialog(self, plane_type: TypeBase | None = None) -> None:
        if plane_type and isinstance(plane_type, TypeBase):
            self.type_combo.setCurrentText(str(plane_type.name))
            self.group_combo.set_filter(plane_type)
            self.group_combo._model.refresh()

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.group_combo.setCurrentText(item.group.name)
        self.system_edit.setText(item.name)

    def add_or_save_item(self) -> None:
        """Save or update system."""
        name = self.system_edit.text().strip()
        group = self.group_combo.currentData()

        if not name:
            self.show_error("Название системы не может быть пустым")
            return

        if group is None:
            self.show_error("Выберите группу обслуживания")
            return

        # Explicitly fetch plane_type to avoid lazy loading issues
        plane_type = group.plane_type

        if self.item:
            self.item.name = name
            self.item.group = group
            self.item.plane_type = plane_type
            self.item.save()
        else:
            SystemBase.create(name=name, group=group, plane_type=plane_type)

        self.updated.emit()
        self.accept()


class AddAgregate(UnAddEditDialog):
    """Dialog for adding/editing aggregate/unit."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Агрегат/Блок")

        self.type_combo = PlaneTypeComboBox()
        self.group_combo = GroupComboBox()
        self.system_combo = SystemComboBox()
        self.agregate_edit = QLineEdit()

        self.group_combo.setEnabled(False)
        self.system_combo.setEnabled(False)
        self.agregate_edit.setEnabled(False)
        self.btn_ok.setEnabled(False)

        self.type_combo.currentIndexChanged.connect(self.update_state)
        self.group_combo.currentIndexChanged.connect(self.update_state)
        self.system_combo.currentIndexChanged.connect(self.update_state)
        self.agregate_edit.textChanged.connect(self.update_state)

        self.type_combo.changed.connect(self.on_type_changed)
        self.group_combo.changed.connect(self.on_group_changed)

        self.form_layout.addRow("Тип самолета:", self.type_combo)
        self.form_layout.addRow("Группа обслуживания:", self.group_combo)
        self.form_layout.addRow("Система самолета:", self.system_combo)
        self.form_layout.addRow("Название блока/агрегата:", self.agregate_edit)

    def on_type_changed(self, plane_type: Any) -> None:
        """Update group combo filter when type changes."""
        if plane_type:
            self.group_combo.set_filter(plane_type)
            self.group_combo._model.refresh()

    def on_group_changed(self, group: Any) -> None:
        """Update system combo filter when group changes."""
        if group:
            self.system_combo.set_filter(group)
            self.system_combo._model.refresh()

    def update_state(self) -> None:
        """Enable/disable fields based on selections."""
        type_selected = self.type_combo.currentData() is not None
        group_selected = self.group_combo.currentData() is not None
        system_selected = self.system_combo.currentData() is not None
        name_filled = bool(self.agregate_edit.text().strip())

        self.group_combo.setEnabled(type_selected)
        self.system_combo.setEnabled(type_selected and group_selected)
        self.agregate_edit.setEnabled(type_selected and group_selected and system_selected)
        self.btn_ok.setEnabled(type_selected and group_selected and system_selected and name_filled)

    def add_dialog(
        self,
        filter_type: TypeBase | None = None,
        filter_group: GroupBase | None = None,
        filter_system: SystemBase | None = None,
    ) -> None:
        """Pre-set filters from parent dialog."""
        if isinstance(filter_type, TypeBase):
            self.type_combo.setCurrentText(str(filter_type.name))
            self.group_combo.set_filter(filter_type)
            self.group_combo._model.refresh()
        if isinstance(filter_group, GroupBase):
            self.group_combo.setCurrentText(str(filter_group.name))
            self.system_combo.set_filter(filter_group)
            self.system_combo._model.refresh()
        if isinstance(filter_system, SystemBase):
            self.system_combo.setCurrentText(str(filter_system.name))

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.system.group.plane_type.name)
        self.group_combo.setCurrentText(item.system.group.name)
        self.system_combo.setCurrentText(item.system.name)
        self.agregate_edit.setText(item.name)

    def add_or_save_item(self) -> None:
        """Save or update agregate."""
        name = self.agregate_edit.text().strip()
        system = self.system_combo.currentData()

        if not name:
            self.show_error("Название агрегата не может быть пустым")
            return

        if system is None:
            self.show_error("Выберите систему")
            return

        # Check if system has valid id
        if not hasattr(system, 'id') or system.id is None:
            self.show_error("Некорректная система: проверьте, что система выбрана корректно")
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
    """Dialog for adding/editing aircraft."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Добавить самолет")

        self.type_combo = PlaneTypeComboBox()
        self.podrazd_combo = PodrazdComboBox()
        self.bort_edit = QLineEdit()
        self.zav_edit = QLineEdit()

        self.form_layout.addRow("Тип самолета", self.type_combo)
        self.form_layout.addRow("Подразделение:", self.podrazd_combo)
        self.form_layout.addRow("Бортовой номер:", self.bort_edit)
        self.form_layout.addRow("Заводской номер:", self.zav_edit)

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.plane_type.name)
        self.podrazd_combo.setCurrentText(item.podrazd.name)
        self.bort_edit.setText(item.bort_number)
        self.zav_edit.setText(item.zav_num)

    def add_or_save_item(self) -> None:
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
                zav_num=zav,
            )

        self.updated.emit()
        self.accept()


# ----------------------------------------------------------------------
# Aircraft Features (Osobennosti) Dialogs
# ----------------------------------------------------------------------
class SettingsOsob(UnDialog):
    """Dialog for managing aircraft features."""

    def __init__(self, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Особенности самолетов")

        self.type_combo = PlaneTypeComboBox()
        self.type_combo.changed.connect(self.on_type_changed)

        self.setup_ui(OsobTable, {"parent": self})
        self.main_layout.insertWidget(0, self.type_combo)

    def on_type_changed(self, plane_type: Any) -> None:
        """Filter table by aircraft type."""
        if plane_type:
            self.table.table_model.load_data(plane_type)
        else:
            self.table.table_model.load_data(None)

    def add_item(self) -> None:
        from app.ui.dialogs.osob_features import OsobFeatureDialog

        dialog = OsobFeatureDialog(parent=self)
        dialog.updated.connect(self.refresh_data)
        if dialog.exec():
            self.updated.emit()

    def edit_item(self, item: Any) -> None:
        from app.ui.dialogs.osob_features import OsobFeatureDialog

        dialog = OsobFeatureDialog(osob=item, parent=self)
        dialog.updated.connect(self.refresh_data)
        if dialog.exec():
            self.updated.emit()

    def delete_item(self, item: Any) -> None:
        self.table.table_model.delete_item(item)
        self.refresh_data()
        self.updated.emit()

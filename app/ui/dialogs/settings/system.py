"""Dialogs for managing aircraft systems."""

from typing import Any

from data.models.aircraft import GroupBase, SystemBase, TypeBase
from PyQt6.QtWidgets import QLineEdit
from app.ui.dialogs.settings.base import UnAddEditDialog, UnDialog
from app.ui.widgets.combo_box import GroupComboBox, PlaneTypeComboBox
from app.ui.widgets.tables import SystemTable


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

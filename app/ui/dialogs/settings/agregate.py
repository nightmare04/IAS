"""Dialogs for managing aggregates/units."""

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLineEdit

from app.ui.dialogs.settings.base import UnAddEditDialog, UnDialog
from app.ui.widgets.combo_box import GroupComboBox, PlaneTypeComboBox, SystemComboBox
from app.ui.widgets.tables import AgregateTable
from data.models.aircraft import AgregateBase, GroupBase, SystemBase, TypeBase


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
            self.agregate_edit.setFocus()
        if isinstance(filter_group, GroupBase):
            self.group_combo.setCurrentText(str(filter_group.name))
            self.system_combo.set_filter(filter_group)
            self.system_combo._model.refresh()
            self.agregate_edit.setFocus()
        if isinstance(filter_system, SystemBase):
            self.system_combo.setCurrentText(str(filter_system.name))
            self.agregate_edit.setFocus()

    def edit_dialog(self, item: Any) -> None:
        super().edit_dialog(item)
        self.type_combo.setCurrentText(item.system.group.plane_type.name)
        self.group_combo.setCurrentText(item.system.group.name)
        self.system_combo.setCurrentText(item.system.name)
        self.agregate_edit.setText(item.name)
        self.agregate_edit.setFocus()

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
